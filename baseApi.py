'''
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>. 
'''
import json
from mysql.connector import pooling
from flask import Flask, jsonify, request
from rfc3986 import validators, uri_reference
from util import get_logger, db_config

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=4, **db_config
)


app = Flask(__name__)

logger = get_logger(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    logger.info("Someone accessed the landing page")
    return "Hi, this is just a landing page"


@app.route("/getPolicies", methods=["GET"])
def getPolicies():
    logger.info("A call to getPolicies was made")
    conn = connection_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id,name,informational_url FROM policy_entries")
    response = cursor.fetchall()
    conn.close()
    logger.info("The call to getPolicies was succesfull")
    return jsonify({"policies": response})


@app.route("/getPolicy/<path:policy>", methods=["GET"])
def getPolicy(policy: str):
    logger.info(f'A call to the getPolicy was made with policy:{policy}')
    if policyValidation(policy):

        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
        WITH contact_agg AS(
        SELECT id,JSON_ARRAYAGG(JSON_OBJECT('type',type,'email', email)) AS contacts
        FROM contacts
        GROUP BY id
        ),
        imp_agg AS(
        SELECT id, JSON_ARRAYAGG(implicit_uri) AS includes_policy_uris
        FROM implicit_policy_uris
        GROUP BY id
        ),
        aug_agg AS(
        SELECT id, JSON_ARRAYAGG(augment_uri) AS augment_policy_uris
        FROM augment_policy_uris
        GROUP BY id    
        ),
        auth_lang_agg AS(
        SELECT auth_id,JSON_ARRAYAGG(JSON_OBJECT('auth_name',auth_name,'language',language)) AS auth_languages
        FROM authority_names
        GROUP BY auth_id
        )
        SELECT p.*, c.contacts AS contacts, 
        imp.includes_policy_uris,
        aug.augment_policy_uris,
        auth_lan.auth_languages,
        auth.uri AS aut
        FROM policy p
        LEFT JOIN contact_agg c ON p.id = c.id
        LEFT JOIN imp_agg imp ON p.id = imp.id
        LEFT JOIN aug_agg aug ON p.id = aug.id
        LEFT JOIN authorities auth ON p.auth_id = auth.auth_id
        LEFT JOIN auth_lang_agg auth_lan ON p.auth_id = auth_lan.auth_id
        WHERE p.id = %s
        """,(policy,))
        response = cursor.fetchone()
        conn.close()
        if response is None:
            return jsonify({"Not a policy id in db": policy})

        # Converting to json list if not None type
        if response["contacts"] is not None:
            response["contacts"] = json.loads(response["contacts"])
        if response["includes_policy_uris"] is not None:
            response["includes_policy_uris"] = json.loads(
                response["includes_policy_uris"]
            )
        if response["augment_policy_uris"] is not None:
            response["augment_policy_uris"] = json.loads(
                response["augment_policy_uris"]
            )
        if response["auth_languages"] is not None:
            response["auth_languages"] = json.loads(
                response["auth_languages"]
            )
        logger.info(f'The call to getPolicy was succesful:{jsonify({"policy": response})}')
        return jsonify({"policy": response})
    else:
        return jsonify({"Not a valid policy": policy})


@app.route("/addPolicy/<string:policy>", methods=["POST"])
def addPolicy(policy: str):

    data = "Attempt to add "
    return jsonify({"data": data + policy})


def policyValidation(policy: str):
    validator = validators.Validator().allow_schemes('http','https','urn').check_validity_of('scheme','path').require_presence_of('scheme')
    uri = uri_reference(policy)
    try:
        validator.validate(uri)
        return True
    except:
        logger.error(f'Invalid policy uri: {policy}')
        return False    


# If to be run with python - uncomment
#if __name__ == "__main__":
#   app.run(debug=False, host='0.0.0.0', port=8080)
