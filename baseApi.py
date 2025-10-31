"""
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>.
"""

import json
import connexion
from mysql.connector import pooling
from util import (
    get_logger,
    db_config,
    CustomIntrospectTokenValidator,
    app_base,
    load_api_spec,
)
from rfc3986 import validators, uri_reference
from connexion.exceptions import OAuthProblem, Unauthorized, Forbidden

from flask import jsonify, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix

# Logging
logger = get_logger(__name__)


# Database connection
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=4, **db_config
)

# Introspection
tokenValidator = CustomIntrospectTokenValidator()


## Commented out for testing
# app.config['SERVER_NAME'] = app_base
# app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


def home():
    """Landing page"""
    logger.info("Someone accessed the landing page")
    return Response(
        "Hi, this is just a landing page", status=200, mimetype="text/plain"
    )


def getPolicies():
    """List all policy entries"""
    logger.info("A call to getPolicies was made")
    conn = connection_pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id,name,informational_url FROM policy_entries")
    response = cursor.fetchall()
    conn.close()
    logger.info("The call to getPolicies was succesfull")
    return jsonify({"policies": response}), 200


def getPolicy(policy: str):
    """Retrieve all information regarding a single policy"""
    logger.info(f"A call to the getPolicy was made with policy:{policy}")
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
        ),
        desc_lang_agg AS(
        SELECT id, JSON_ARRAYAGG(JSON_OBJECT('description',description,'language',language)) AS description_languages
        FROM descriptions
        GROUP BY id
        )
        SELECT p.policy_url,
        p.valid_from,
        p.ttl,
        p.policy_class,
        p.notice_refresh_period,
        p.id,
        c.contacts AS contacts, 
        imp.includes_policy_uris,
        aug.augment_policy_uris,
        auth_lan.auth_languages,
        desc_lang.description_languages,
        auth.uri AS aut,
        priv_pol.jurisdiction AS policy_jurisdiction
        FROM policy p
        LEFT JOIN contact_agg c ON p.id = c.id
        LEFT JOIN imp_agg imp ON p.id = imp.id
        LEFT JOIN aug_agg aug ON p.id = aug.id
        LEFT JOIN desc_lang_agg desc_lang ON p.id = desc_lang.id
        LEFT JOIN privacy_policies priv_pol ON p.id = priv_pol.id
        LEFT JOIN authorities auth ON p.auth_id = auth.auth_id
        LEFT JOIN auth_lang_agg auth_lan ON p.auth_id = auth_lan.auth_id
        WHERE p.id = %s
        """,
            (policy,),
        )
        response = cursor.fetchone()
        conn.close()
        if response is None:
            return jsonify({"Not a policy id in db": policy}), 404

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
            response["auth_languages"] = json.loads(response["auth_languages"])
        if response["description_languages"] is not None:
            response["description_languages"] = json.loads(
                response["description_languages"]
            )
        logger.info(f"The call to getPolicy was succesful:{response}")
        return jsonify({"policy": response}), 200
    else:
        return jsonify({"Not a valid policy": policy}), 400


def addPolicy():
    """Add a new policy (requires OAuth2 token with scope openid for now)"""
    data = request.get_json()
    logger.info(f"Received data: {data}")

    return jsonify({"Success": "True", "received": data}), 200


def policyValidation(policy: str):
    validator = (
        validators.Validator()
        .allow_schemes("http", "https", "urn")
        .check_validity_of("scheme", "path")
        .require_presence_of("scheme")
    )
    uri = uri_reference(policy)
    try:
        validator.validate(uri)
        return True
    except:
        logger.error(f"Invalid policy uri: {policy}")
        return False


def introspectToken(token, required_scopes=None, request=None):
    """
    Connexion x-tokenInfoFunc
    Returns a dictionary with token info if valid, returns Unauthorized or Forbidden if invalid
    """
    try:
        logger.info(f"Token:{token}")
        info = tokenValidator.introspect_token(token)
        logger.info(f"Token info:{info}")

        if not tokenValidator.validate_aud(info):
            raise Forbidden("Wrong audiance")

        if not tokenValidator.validate_claim(token):
            raise Forbidden("Missing required roles")

        if not info.get("active", False):
            raise Unauthorized("Inactive token")

        if required_scopes:
            token_scopes = info.get("scope", "").split()
            if not set(required_scopes).issubset(token_scopes):
                raise Forbidden("Missing required scopes")

        return info
    except Exception as e:
        logger.error(f"Token introspection failed: {e}")
        raise


app = connexion.FlaskApp(__name__, specification_dir="./")
spec = load_api_spec()
app.add_api(specification=spec, strict_validation=True)
