import pytest
import requests
from dbInit import db_config


connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool", pool_size=4, **db_config
)


def testLandingPage():
    response = requests.get('http://localhost:8080/')

    assert response == 'Hi, this is just a landing page'