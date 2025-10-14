'''
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>. 
'''
import pytest
import requests
import os
import mysql.connector


baseUrl = os.environ.get("APP_URL")


db_config = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "port": int(os.environ.get("DB_PORT")),
    "database": os.environ.get("DB_NAME"),
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()


landingPage = "Hi, this is just a landing page"
 
#getPolicies =f'''{{"policies":[{{"informational_url":"{baseUrl}/getPolicy/4a6d33b3-34c0-4d39-9c87-f39d6f932a6b","name":"AARC documentation example2","uri":"4a6d33b3-34c0-4d39-9c87-f39d6f932a6b"}},{{"informational_url":"{baseUrl}/getPolicy/8eaa6f4e-bf42-4cb4-8048-e26864c7ec58","name":"AARC documentation example","uri":"8eaa6f4e-bf42-4cb4-8048-e26864c7ec58"}}]}}\n'''
getPolicies =f'''{{"policies":[{{"id":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","informational_url":"{baseUrl}/getPolicy/https%3A%2F%2Foperations-portal.egi.eu%2Fvo%2Fview%2Fvoname%2Fxenon.biggrid.nl","name":"AARC documentation example2"}},{{"id":"urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","informational_url":"{baseUrl}/getPolicy/urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","name":"AARC documentation example"}}]}}\n'''



#policy1 = '''{"policy":{"augment_policy_uris":["https://wise-community.org/wise-baseline-aup/v1/"],"aut":"https://xenonexperiment.org/","auth_name":"Xenon-nT collaboration","contacts":[{"email":"grid.support@nikhef.nl","type":"standard"},{"email":"vo-xenon-admins@biggrid.nl","type":"security"}],"description":"detector construction and experiment analysis for the search of dark matter using Xenon detectors","id":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","includes_policy_uris":null,"notice_refresh_period":null,"policy_class":"purpose","policy_url":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","ttl":31557600,"uri":"4a6d33b3-34c0-4d39-9c87-f39d6f932a6b","valid_from":"Fri, 29 Jul 2011 00:00:00 GMT"}}\n'''
policy1 = '''{"policy":{"augment_policy_uris":["https://wise-community.org/wise-baseline-aup/v1/"],"aut":"https://xenonexperiment.org/","auth_name":"Xenon-nT collaboration","contacts":[{"email":"grid.support@nikhef.nl","type":"standard"},{"email":"vo-xenon-admins@biggrid.nl","type":"security"}],"description":"detector construction and experiment analysis for the search of dark matter using Xenon detectors","id":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","includes_policy_uris":null,"notice_refresh_period":null,"policy_class":"purpose","policy_url":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","ttl":31557600,"valid_from":"Fri, 29 Jul 2011 00:00:00 GMT"}}\n'''


#policy2 = '''{"policy":{"augment_policy_uris":null,"aut":"https://www.nikhef.nl/","auth_name":"Nikhef","contacts":[{"email":"abuse@nikhef.nl","type":"security"},{"email":"helpldesk@nikhef.nl","type":"standard"},{"email":"information-security@nikhef.nl","type":"standard"},{"email":"privacy@nikhef.nl","type":"privacy"}],"description":"This Acceptable Use Policy governs the use of the Nikhef networking and computer services; all users of these services are expected to understand and comply to these rules.","id":"urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","includes_policy_uris":["https://documents.egi.eu/document/2623"],"notice_refresh_period":34214400,"policy_class":"acceptable-use","policy_url":"https://www.nikhef.nl/aup/","ttl":604800,"uri":"8eaa6f4e-bf42-4cb4-8048-e26864c7ec58","valid_from":"Mon, 04 Apr 2022 00:00:00 GMT"}}\n'''
policy2 = '''{"policy":{"augment_policy_uris":null,"aut":"https://www.nikhef.nl/","auth_name":"Nikhef","contacts":[{"email":"helpldesk@nikhef.nl","type":"standard"},{"email":"information-security@nikhef.nl","type":"standard"},{"email":"abuse@nikhef.nl","type":"security"},{"email":"privacy@nikhef.nl","type":"privacy"}],"description":"This Acceptable Use Policy governs the use of the Nikhef networking and computer services; all users of these services are expected to understand and comply to these rules.","id":"urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","includes_policy_uris":["https://documents.egi.eu/document/2623"],"notice_refresh_period":34214400,"policy_class":"acceptable-use","policy_url":"https://www.nikhef.nl/aup/","ttl":604800,"valid_from":"Mon, 04 Apr 2022 00:00:00 GMT"}}\n'''


tables = '''[('augment_policy_uris',), ('authorities',), ('contacts',), ('implicit_policy_uris',), ('policy',), ('policy_entries',)]'''


def testLandingPage():
    response = requests.get(baseUrl)

    assert response.text == landingPage


def testGetPolicy1():
    response = requests.get(baseUrl+"/getPolicy/4a6d33b3-34c0-4d39-9c87-f39d6f932a6b")

    assert response.text == policy1

def testGetPolicy2():
    response = requests.get(baseUrl+"/getPolicy/8eaa6f4e-bf42-4cb4-8048-e26864c7ec58")

    assert response.text == policy2


def testGetPolicies():
    response = requests.get(baseUrl+'/getPolicies')

    assert response.text == getPolicies

