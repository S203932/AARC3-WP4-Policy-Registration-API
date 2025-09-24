import pytest
import requests

db_config = {
    "host": get_env_variable("DB_HOST", required=True),
    "user": get_env_variable("DB_USER", required=True),
    "password": get_env_variable("DB_PASSWORD", required=True),
    "port": int(get_env_variable("DB_PORT", required=True)),
    "database": get_env_variable("DB_NAME", required=True),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=4, **db_config
)


def testLandingPage():
    response = requests.get('http://localhost:8080/')

    assert response == 'Hi, this is just a landing page'