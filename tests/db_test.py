import pytest
import requests
import os
import mysql.connector


baseUrl = os.environ.get("APP_URL")


def testLandingPage():
    response = requests.get(baseUrl)

    assert response.text == "Hi, this is just a landing page"



