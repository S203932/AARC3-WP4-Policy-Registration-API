from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import pooling
import uuid
import json
from util import get_logger
from dbInit import db_config, init_db

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=4, **db_config
)

# Init test data
init_db(connection_pool)

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
    cursor.execute("SELECT uri,name,informational_url FROM policy_entries")
    response = cursor.fetchall()
    conn.close()
    logger.info("The call to getPolicies was succesfull")
    return jsonify({"policies": response})


@app.route("/getPolicy/<string:policy>", methods=["GET"])
def getPolicy(policy: str):
    logger.info("A call to the getPolicy was made")
    if uuid_validation(policy):

        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
        WITH contact_agg AS(
        SELECT policy_uri,JSON_ARRAYAGG(JSON_OBJECT('type',type,'email', email)) AS contacts
        FROM contacts
        GROUP BY policy_uri
        ),
        imp_agg AS(
        SELECT uri, JSON_ARRAYAGG(implicit_uri) AS includes_policy_uris
        FROM implicit_policy_uris
        GROUP BY uri
        ),
        aug_agg AS(
        SELECT uri, JSON_ARRAYAGG(augment_uri) AS augment_policy_uris
        FROM augment_policy_uris
        GROUP BY uri    
        )
        SELECT p.*, c.contacts AS contacts, 
        imp.includes_policy_uris,
        aug.augment_policy_uris,
        auth.uri AS aut
        FROM policy p
        LEFT JOIN contact_agg c ON p.uri = c.policy_uri
        LEFT JOIN imp_agg imp ON p.uri = imp.uri
        LEFT JOIN aug_agg aug ON p.uri = aug.uri
        LEFT JOIN authorities auth ON p.auth_name = auth.auth_name
        WHERE p.uri = '{uri}'
        """.format(
                uri=policy
            )
        )
        response = cursor.fetchone()
        conn.close()
        if response is None:
            return jsonify({"Not a uuid in db": policy})

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
        logger.info("The call to getPolicy was succesful")
        return jsonify({"policy": response})
    else:
        return jsonify({"Not uuid": policy})


@app.route("/addPolicy/<string:policy>", methods=["POST"])
def addPolicy(policy: str):

    data = "Attempt to add "
    return jsonify({"data": data + policy})


def uuid_validation(policy: str):
    try:
        uuid.UUID(policy, version=4)
        return True
    except ValueError:
        return False


# If to be run with python - uncomment
#if __name__ == "__main__":
#   app.run(debug=False, host='0.0.0.0', port=8080)
