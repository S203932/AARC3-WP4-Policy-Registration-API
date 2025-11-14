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

appendixB1 = '''{"policy":{"augment_policy_uris":null,"aut":"https://www.nikhef.nl/","aut_name":"Nikhef","contacts":[{"email":"helpdesk@nikhef.nl","type":"standard"},{"email":"information-security@nikhef.nl","type":"standard"},{"email":"abuse@nikhef.nl","type":"security"},{"email":"privacy@nikhef.nl","type":"privacy"}],"description":"This Acceptable Use Policy governs the use of the Nikhef networking and computer services; all users of these services are expected to understand and comply to these rules.","description#nl_NL":"Deze Gebruiksvoorwaarden betreffen het gebruik van netwerk en computers bij Nikhef. Iedere gebruiker van deze middelen of diensten wordt geacht op hoogte te zijn van deze voorwaarden en deze na te leven.","id":"urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","includes_policy_uris":["https://documents.egi.eu/document/2623"],"notice_refresh_period":34214400,"policy_class":"acceptable-use","policy_url":"https://www.nikhef.nl/aup/","ttl":604800,"valid_from":"2022-04-04T00:00:00Z"}}\n'''

appendixB2 = '''{"policy":{"augment_policy_uris":["https://wise-community.org/wise-baseline-aup/v1/"],"aut":"https://xenonexperiment.org/","aut_name":"Xenon-nT collaboration","aut_name#dk_DK":"Xenon-nT samarbejde","contacts":[{"email":"grid.support@nikhef.nl","type":"standard"},{"email":"vo-xenon-admins@biggrid.nl","type":"security"}],"description":"detector construction and experiment analysis for the search of dark matter using Xenon detectors","id":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","includes_policy_uris":null,"notice_refresh_period":null,"policy_class":"purpose","policy_url":"https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl","ttl":31557600,"valid_from":"2011-07-29T00:00:00Z"}}\n'''

minimumPolicy = '''{"policy":{"augment_policy_uris":null,"aut":null,"aut_name":"Sicherheit fur dich","contacts":[{"email":"Max.Jurgen@hochschule.de","type":"standard"}],"id":"urn:som:654321","includes_policy_uris":null,"notice_refresh_period":null,"policy_class":"privacy","policy_url":null,"ttl":null,"valid_from":null}}\n'''

somePolicy = '''{"policy":{"augment_policy_uris":["https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl"],"aut":"https://xenonexperiment.org/","aut_name":"Xenon-nT collaboration","aut_name#dk_DK":"Xenon-nT samarbejde","contacts":[{"email":"research.support@somewhere.org","type":"standard"},{"email":"secure@somewhere.org","type":"security"},{"email":"safe@somewhere.org","type":"privacy"}],"description":"A community somwhere researching for the betterment of mankind (hopefully)","description#dk_DK":"Et samarbejde et eller andet sted som forsker til fordel for menneskeheden (forhaabentlig)","id":"https://some-community.org","includes_policy_uris":["urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815","urn:idk:123456"],"notice_refresh_period":41212301,"policy_class":"privacy#eu","policy_url":"https://some-community.org","ttl":21817600,"valid_from":"2025-10-17T09:00:00Z"}}\n'''

anotherPolicy = '''{"policy":{"augment_policy_uris":["https://documents.egi.eu/document/2623"],"aut":"https://cern.ch","aut_name":"CERN","aut_name#dk_DK":"CERN","contacts":[{"email":"notSupicious@mikrosoft.xyz","type":"standard"}],"description":"A research community beyond suspicion.","description#dk_DK":"Et trovaerdigt forsknings institut.","id":"https://another-community.org","includes_policy_uris":["https://some-community.org","https://wise-community.org/wise-baseline-aup/v1/"],"notice_refresh_period":null,"policy_class":"sla","policy_url":"https://another-community.org","ttl":31104300,"valid_from":"2019-06-10T23:59:59Z"}}\n'''

thePolicy = '''{"policy":{"augment_policy_uris":["urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815"],"aut":null,"aut_name#dk_DK":"Auto sikkerhed","contacts":[{"email":"friend@gov.org","type":"standard"}],"id":"urn:idk:123456","includes_policy_uris":["https://another-community.org"],"notice_refresh_period":259200,"policy_class":"conditions","policy_url":"https://the-community.org","ttl":604800,"valid_from":"2025-05-01T18:00:00Z"}}\n'''

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
