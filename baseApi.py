"""
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>.
"""

import json
import connexion
import urllib.parse
from mysql.connector import pooling, errors
from util import (
    get_logger,
    db_config,
    CustomIntrospectTokenValidator,
    app_base,
    load_api_spec,
    api_base
)
from rfc3986 import validators, uri_reference
from connexion.exceptions import OAuthProblem, Unauthorized, Forbidden
from policy_entry.policy.policy import Policy
from policy_entry.policyEntry import PolicyEntry

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

        logger.info(f'Response: {response}')
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
            response["descriptions"] = json.loads(
                response["description_languages"]
            )

        policyObject = Policy.from_dict(response)
        policyDict = policyObject.to_dict()


        logger.info(f"The call to getPolicy was succesful:{policyDict}")
        return jsonify({"policy": policyDict}), 200
    else:
        return jsonify({"Not a valid policy": policy}), 400


def addPolicy():
    """Add a new policy (requires OAuth2 token with scope openid for now)"""
    data = request.get_json()
    logger.info(f"Received data: {data}")

    policy_raw = data["policy"]
    policyEntry_raw = data["policy_entry"]

    policy = Policy.from_dict(policy_raw)
    policyEntry = PolicyEntry.from_dict(policyEntry_raw)

    insertPolicy(policy, policyEntry)


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
    
def sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, str):
        return f'"{value}"'
    return value

def insertPolicy(policy:Policy, policyEntry: PolicyEntry):

    
    logger.info(f'aut: {policy.authority.aut}')
    authority = f'INSERT INTO authorities(uri) VALUES ("{policy.authority.aut}") '
    authorityId = f'SELECT auth_id FROM authorities WHERE uri = "{policy.authority.aut}"'


    conn = connection_pool.get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    # Inserting the authority
    try:
        logger.info(f'authority: {authority}')
        cursor.execute(authority)
        logger.info(f"Following command succeded:{authority[:30]}")
    except errors.IntegrityError as err:
        logger.error(f"Failed duplicate command: {authority[:30]}")


    # Getting the id from the authority table
    cursor.execute(authorityId)
    auth_id = cursor.fetchone()

    logger.info(f'Managed to get auth_id: {auth_id}')
    logger.info(f'The type: {type(auth_id)}')

    # Inserting authority names
    for auth in policy.authority.names:
        tempLang = f'INSERT INTO authority_names(auth_id, language, auth_name) VALUES ({auth_id.get("auth_id")}, "{auth.language}", "{auth.aut_name}");'
        logger.info(f'authorityNames: {tempLang}')
        try:
            cursor.execute(tempLang)
            logger.info(f"Following command succeded:{tempLang[:30]}")
        except errors.IntegrityError as err:
            logger.error(f"Failed duplicate command: {tempLang[:30]}")


    # Inserting into policy entry
    informational_url = api_base + "/getPolicy/" + urllib.parse.quote(policy.policyId, safe=' ')
    try: 
        policyEntry = f'INSERT INTO policy_entries(id, name, informational_url, owner) VALUES ("{policy.policyId}", "{policyEntry.name}", "{informational_url}", "{policyEntry.owner}");'
        logger.info(f'Policy: {policyEntry}')
        logger.info(f"Following command succeded:{policyEntry[:30]}")
        cursor.execute(policyEntry)
    except errors.IntegrityError as err:
        logger.error(f"Failed duplicate command: {policyEntry[:30]}")


    # Inserting the policy
    try:
        policyInsert = (
            f'INSERT INTO policy('
            f'id, policy_url, auth_id, valid_from, ttl, policy_class, notice_refresh_period'
            f') VALUES ('
            f'{sql_value(policy.policyId)}, '
            f'{sql_value(policy.policy_url)}, '
            f'{sql_value(auth_id.get("auth_id"))}, '
            f'{sql_value(policy.valid_from)}, '
            f'{sql_value(policy.ttl)}, '
            f'{sql_value(policy.policy_class)}, '
            f'{sql_value(policy.notice_refresh_period)}'
            f');'
        ) 
        logger.info(f'Policy: {policyInsert}')
        cursor.execute(policyInsert)
        logger.info(f"Following command succeded:{policyInsert[:30]}")
    except errors.IntegrityError as err:
        logger.error(f"Failed duplicate command: {policyInsert[:30]}")


    # Inserting the descriptions
    for description in policy.descriptions:
        tempDesc = f'INSERT INTO descriptions(id, description, language) VALUES ("{policy.policyId}", "{description.description}", "{description.language}");'
        logger.info(f'description: {tempDesc}')
        try:
            cursor.execute(tempDesc)
            logger.info(f"Following command succeded:{tempDesc[:30]}")
        except errors.IntegrityError as err:
            logger.error(f"Failed duplicate command: {tempDesc[:30]}")

    # Inserting the jurisdiction
    if policy.policy_jurisdiction is not None:
        tempJur = f'INSERT INTO privacy_policies(id, jurisdiction) VALUES ("{policy.policyId}", "{policy.policy_jurisdiction}");'
        logger.info(f'Jurisdiction: {tempJur}')
        try:
            cursor.execute(tempJur)
            logger.info(f"Following command succeded:{tempJur[:30]}")
        except errors.IntegrityError as err:
            logger.error(f"Failed duplicate command: {tempJur[:30]}")


    # Inserting the contacts 
    for contact in policy.contacts:
        tempCon = f'INSERT INTO contacts(type, email, id) VALUES ("{contact.contact_type}", "{contact.email}", "{policy.policyId}");'
        logger.info(f'contact: {tempCon}')
        try:
            cursor.execute(tempCon)
            logger.info(f"Following command succeded:{tempCon[:30]}")
        except errors.IntegrityError as err:
            logger.error(f"Failed duplicate command: {tempCon[:30]}")

    # Inserting the implicit policies
    if policy.implicit_policy_uris is not None:
        for implicit in policy.implicit_policy_uris:
            tempImpl = f'INSERT INTO implicit_policy_uris(id, implicit_uri) VALUES ("{policy.policyId}", "{implicit}");'
            logger.info(f'implicit: {tempImpl}')
            try:
                cursor.execute(tempImpl)
                logger.info(f"Following command succeded:{tempImpl[:30]}")
            except errors.IntegrityError as err:
                logger.error(f"Failed duplicate command: {tempImpl[:30]}")


    # Inserting the augment policies
    if policy.augment_policy_uris is not None:
        for augment in policy.augment_policy_uris:
            tempAugm = f'INSERT INTO augment_policy_uris(id, augment_uri) VALUES ("{policy.policyId}", "{augment}");'
            logger.info(f'Augment: {tempAugm}')
            try:
                cursor.execute(tempAugm)
                logger.info(f"Following command succeded:{tempAugm[:30]}")
            except errors.IntegrityError as err:
                logger.error(f"Failed duplicate command: {tempAugm[:30]}")

    conn.commit()
    conn.close()


app = connexion.FlaskApp(__name__, specification_dir="./")
spec = load_api_spec()
app.add_api(specification=spec, strict_validation=True)
