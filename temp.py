from flask import Flask, jsonify, request
import mysql.connector
import uuid
import json


mydb = mysql.connector.connect(
    database="",
    host="",
    user="",
    password="",
    port=0,
)

cursor = mydb.cursor(dictionary=True)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return "Hi, this is just a landing page"

@app.route("/getPolicies", methods=["GET"])
def getPolicies():
    cursor.execute("SELECT uri,name,informational_url FROM policy_entries")
    response = cursor.fetchall()
    return jsonify({"policies": response})


@app.route("/getPolicy/<string:policy>", methods=["GET"])
def getPolicy(policy: str):
    if uuid_validation(policy):
        cursor.execute('''
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
        auth.auth_name
        FROM policy p
        LEFT JOIN contact_agg c ON p.uri = c.policy_uri
        LEFT JOIN imp_agg imp ON p.uri = imp.uri
        LEFT JOIN aug_agg aug ON p.uri = aug.uri
        LEFT JOIN authorities auth ON p.auth = auth.uri
        WHERE p.uri = '{uri}'
        '''.format(uri=policy)
        )
        response = cursor.fetchone()

        # Converting to json list if not None type
        if response["contacts"] is not None:
            response["contacts"] = json.loads(response["contacts"])
        if response["includes_policy_uris"] is not None:
            response["includes_policy_uris"] = json.loads(response["includes_policy_uris"])
        if response["augment_policy_uris"] is not None:
            response["augment_policy_uris"] = json.loads(response["augment_policy_uris"])

        return jsonify({"policy": response})
    else:
        return jsonify({"Not uuid": policy})

    return jsonify({"data": policy, "someOtherInfo": "whichIsRelevant"})


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


if __name__ == "__main__":
    app.run(debug=False)
