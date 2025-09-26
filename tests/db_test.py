import pytest
import requests
import os
import mysql.connector


baseUrl = os.environ.get("APP_URL")

getPolicies ="""{
  "policies": [
    {
      "informational_url": "{baseurl}/getPolicy/4a6d33b3-34c0-4d39-9c87-f39d6f932a6b",
      "name": "AARC documentation example2",
      "uri": "4a6d33b3-34c0-4d39-9c87-f39d6f932a6b"
    },
    {
      "informational_url": "https://base-api-notice-management-api.app.cern.ch/getPolicy/8eaa6f4e-bf42-4cb4-8048-e26864c7ec58",
      "name": "AARC documentation example",
      "uri": "8eaa6f4e-bf42-4cb4-8048-e26864c7ec58"
    }
  ]
}
"""

def testLandingPage():
    response = requests.get(baseUrl)

    assert response.text == "Hi, this is just a landing page"


def get


def testGetPolicies():
    response = requests.get(baseUrl+'/getPolicies')

    assert response.text == 'THis will fail on purpose'

