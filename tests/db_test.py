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
 
getPolicies = f'''{{"policies":[{{"id":"https://another-community.org","informational_url":"{baseUrl}/getPolicy/https%3A%2F%2Fanother-community.org","name":"Another community"}},{{"id":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","informational_url":"{baseUrl}/getPolicy/https%3A%2F%2Foperations-portal.egi.eu%2Fvo%2Fview%2Fvoname%2Fxenon.biggrid.nl","name":"Xenon biggrid"}},{{"id":"https://some-community.org","informational_url":"{baseUrl}/getPolicy/https%3A%2F%2Fsome-community.org","name":"Some community"}},{{"id":"urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","informational_url":"{baseUrl}/getPolicy/urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","name":"Nikhef"}},{{"id":"urn:idk:123456","informational_url":"{baseUrl}/getPolicy/urn:idk:123456","name":"The community"}},{{"id":"urn:som:654321","informational_url":"{baseUrl}/getPolicy/urn:som:654321","name":"Minimum info policy"}}]}}\n'''

appendixB1 = '''{"policy":{"augment_policy_uris":null,"aut":"https://www.nikhef.nl/","auth_languages":[{"auth_name":"Nikhef","language":"stand"}],"contacts":[{"email":"helpdesk@nikhef.nl","type":"standard"},{"email":"information-security@nikhef.nl","type":"standard"},{"email":"abuse@nikhef.nl","type":"security"},{"email":"privacy@nikhef.nl","type":"privacy"}],"description_languages":[{"description":"Deze Gebruiksvoorwaarden betreffen het gebruik van netwerk en computers bij Nikhef. Iedere gebruiker van deze middelen of diensten wordt geacht op hoogte te zijn van deze voorwaarden en deze na te leven.","language":"nl_NL"},{"description":"This Acceptable Use Policy governs the use of the Nikhef networking and computer services; all users of these services are expected to understand and comply to these rules.","language":"stand"}],"id":"urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","includes_policy_uris":["https://documents.egi.eu/document/2623"],"notice_refresh_period":34214400,"policy_class":"acceptable-use","policy_jurisdiction":null,"policy_url":"https://www.nikhef.nl/aup/","ttl":604800,"valid_from":"Mon, 04 Apr 2022 00:00:00 GMT"}}\n'''

appendixB2 = '''{"policy":{"augment_policy_uris":["https://wise-community.org/wise-baseline-aup/v1/"],"aut":"https://xenonexperiment.org/","auth_languages":[{"auth_name":"Xenon-nT samarbejde","language":"dk_DK"},{"auth_name":"Xenon-nT collaboration","language":"stand"}],"contacts":[{"email":"grid.support@nikhef.nl","type":"standard"},{"email":"vo-xenon-admins@biggrid.nl","type":"security"}],"description_languages":[{"description":"detector construction and experiment analysis for the search of dark matter using Xenon detectors","language":"stand"}],"id":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","includes_policy_uris":null,"notice_refresh_period":null,"policy_class":"purpose","policy_jurisdiction":null,"policy_url":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","ttl":31557600,"valid_from":"Fri, 29 Jul 2011 00:00:00 GMT"}}\n'''

minimumPolicy = '''{"policy":{"augment_policy_uris":null,"aut":null,"auth_languages":[{"auth_name":"Sicherheit fur dich","language":"stand"}],"contacts":[{"email":"Max.Jurgen@hochschule.de","type":"standard"}],"description_languages":null,"id":"urn:som:654321","includes_policy_uris":null,"notice_refresh_period":null,"policy_class":"privacy","policy_jurisdiction":null,"policy_url":null,"ttl":null,"valid_from":null}}\n'''

somePolicy = '''{"policy":{"augment_policy_uris":["https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl"],"aut":"https://xenonexperiment.org/","auth_languages":[{"auth_name":"Xenon-nT samarbejde","language":"dk_DK"},{"auth_name":"Xenon-nT collaboration","language":"stand"}],"contacts":[{"email":"research.support@somewhere.org","type":"standard"},{"email":"secure@somewhere.org","type":"security"},{"email":"safe@somewhere.org","type":"privacy"}],"description_languages":[{"description":"Et samarbejde et eller andet sted som forsker til fordel for menneskeheden (forhaabentlig)","language":"dk_DK"},{"description":"A community somwhere researching for the betterment of mankind (hopefully)","language":"stand"}],"id":"https://some-community.org","includes_policy_uris":["urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","urn:idk:123456"],"notice_refresh_period":41212301,"policy_class":"privacy","policy_jurisdiction":"eu","policy_url":"https://some-community.org","ttl":21817600,"valid_from":"Fri, 17 Oct 2025 09:00:00 GMT"}}\n'''

anotherPolicy = '''{"policy":{"augment_policy_uris":["https://documents.egi.eu/document/2623"],"aut":"https://cern.ch","auth_languages":[{"auth_name":"CERN","language":"dk_DK"},{"auth_name":"CERN","language":"stand"}],"contacts":[{"email":"notSupicious@mikrosoft.xyz","type":"standard"}],"description_languages":[{"description":"Et trovaerdigt forsknings institut.","language":"dk_DK"},{"description":"A research community beyond suspicion.","language":"stand"}],"id":"https://another-community.org","includes_policy_uris":["https://some-community.org","https://wise-community.org/wise-baseline-aup/v1/"],"notice_refresh_period":null,"policy_class":"sla","policy_jurisdiction":null,"policy_url":"https://another-community.org","ttl":31104300,"valid_from":"Mon, 10 Jun 2019 23:59:59 GMT"}}\n'''

thePolicy = '''{"policy":{"augment_policy_uris":["urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815"],"aut":null,"auth_languages":[{"auth_name":"Auto sikkerhed","language":"dk_DK"}],"contacts":[{"email":"friend@gov.org","type":"standard"}],"description_languages":null,"id":"urn:idk:123456","includes_policy_uris":["https://another-community.org"],"notice_refresh_period":259200,"policy_class":"conditions","policy_jurisdiction":null,"policy_url":"https://the-community.org","ttl":604800,"valid_from":"Thu, 01 May 2025 18:00:00 GMT"}}\n'''

def testLandingPage():
    response = requests.get(baseUrl)

    assert response.text == landingPage

def testGetPolicies():
    response = requests.get(baseUrl+'/getPolicies')

    assert response.text == getPolicies

def testGetPolicyAppendixB1():
    response = requests.get(baseUrl+"/getPolicy/urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815")

    assert response.text == appendixB1

def testGetPolicyAppendixB2():
    response = requests.get(baseUrl+"/getPolicy/https%3A%2F%2Foperations-portal.egi.eu%2Fvo%2Fview%2Fvoname%2Fxenon.biggrid.nl")

    assert response.text == appendixB2

def testGetPolicyMinimum():
    response = requests.get(baseUrl + '/getPolicy/urn:som:654321')

    assert response.text == minimumPolicy

def testGetPolicySome():
    response = requests.get(baseUrl + '/getPolicy/https%3A%2F%2Fsome-community.org')

    assert response.text == somePolicy    

def testGetPolicyAnother():
    response = requests.get(baseUrl + '/getPolicy/https%3A%2F%2Fanother-community.org')

    assert response.text == anotherPolicy    

def testGetPolicyThe():
    response = requests.get(baseUrl + '/getPolicy/urn:idk:123456')

    assert response.text == thePolicy    