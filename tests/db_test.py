import pytest
import requests
import os
from mysql.connector import pooling

db_config = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "port": int(os.environ.get("DB_PORT")),
    "database": os.environ.get("DB_NAME"),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=4, **db_config
)


def testLandingPage():
    response = requests.get("http://localhost:8080/")

    assert response == "Hi, this is just a landing page"
