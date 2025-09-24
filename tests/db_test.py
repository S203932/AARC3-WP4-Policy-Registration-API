import pytest
import requests
import os


baseUrl = os.environ.get("APP_URL")


def testLandingPage():
    response = requests.get(baseUrl)

    assert response == "Hi, this is just a landing page"
