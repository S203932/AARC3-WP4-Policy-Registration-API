import pytest
import requests
import os
import mysql.connector



db_config = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "port": int(os.environ.get("DB_PORT")),
    "database": os.environ.get("DB_NAME")
}


db = mysql.connector.connect(
    host = os.environ.get("DB_HOST"),
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASSWORD"),
    port = int(os.environ.get("DB_PORT")),
    database = os.environ.get("DB_NAME")
)


cursor.execute("SHOW DATABASES")

for x in cursor:
  print(x) 


""" baseUrl = os.environ.get("APP_URL")


def testLandingPage():
    response = requests.get(baseUrl)

    assert response == "Hi, this is just a landing page"
 """


