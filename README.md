# AARC3-WP4-Policy-Registration-API
This is a base implementation of a policy registry API in accordance with AARC-G083

# Requirements to run the api
- A mysql database that has the following structure as seen below.
  - This database will be initiliazied and populated with dummy data provided one uses the docker image.  
- An IDP capable of doing the OAuth implicit flow and token introspection in accordance with OAuth
  - This is to verify the user when adding a policy. The swagger ui implemented is capable of doing the implicit flow, but if you have another service that can provide tokens, then it is not required for the IDP to be capable of doing the implicit flow. 
  - However, the token introspection is a must and therefore all information related to the IDP introspection must be provided. 

## Structure of the required database
The database that will be created when running the api will have the following structure. 
![Alt text](images/API_DB_class.jpg?raw=true "Title")

Within the api is an initialization script of the database that will create the above mentioned tables and populate them with some dummy data. 

# How to run the api
There are different ways to run the api. True for all of them is that one needs to provide the database information to the api. 
The database information that needs to be provided are the following:
- `DB_HOST=the_AARC_DB`
- `DB_USER=the_AARC_User`
- `DB_PASSWORD=the_AARC_User_Password`
- `DB_PORT=the_AARC_DB_Port`
- `DB_NAME=name_of_the_database`

Furthermore, one needs to provide the following information about where the api is to be hosted:
- `APP_URL=base_link_for_the_api_with_scheme`
- `APP_BASE=base_link_for_the_api_without_scheme`

Lastly, one needs to provide the following information about the IDP used for authentication to add a policy to the registry:
- `IDP_AUTHORIZATION_ENDPOINT=https://somewhere.org/openid-connect/auth`
- `IDP_TOKEN_ENDPOINT=https://somewhere.org/openid-connect/token`
- `IDP_INTROSPECTION_ENDPOINT=https://somewhere.org/openid-connect/token/introspect`
- `CLAIM_PATH=path_to_the_claim_in_token`
- `IDP_ID = client_id_for_idp`
- `IDP_SECRET = client_secret_for_idp`

Given that one has an external service to provide the tokens one can resort to only provide dummy values for the following environment variables:
- `IDP_AUTHORIZATION_ENDPOINT`
- `IDP_TOKEN_ENDPOINT`

These are the following ways to run the api.

## Docker image
- Pull the newest image from the [Packages](https://github.com/S203932/AARC3-WP4-Policy-Registration-API/pkgs/container/aarc3-wp4-policy-registration-api%2Fpolicy-registry)
- When deploying the image on kubernetes or your given platform, provide the aformentioned database, api and IDP information.

## Docker compose
- One can use docker compose given that one populates the `.env` first with the database, api and IDP information. 
- Alternatively, one provide the db information at runtime.
For using docker compose, one can provide the following database and api information:
- `DB_HOST=mysql-db`
- `DB_USER=testuser`
- `DB_PASSWORD=testpass`
- `DB_PORT=3306`
- `DB_NAME=testdb`
- `APP_URL=http://127.0.0.1:8080`
- `APP_BASE=localhost:8080`
One would still need to provide the previously mentioned IDP information. 

# Api Endpoints
The following are the available endpoints of the api. 

## /getPolicies
The endpoint `/getPolicies` presents a list of all the available policies in json format.
One can only use a `GET` operation at this endpoint.
For each policy one will be presented with the `name`, `uri` and `information_url`.
- name - the name of the policy
- uri - the uri of the given policy 
- information_url - a link to get further information about the given policy from the api. The link is `/getPolicy/<uri>`.

The following is an example of policies returned from the given endpoint.
```json
{
  "policies": [
    {
      "id": "https://another-community.org",
      "informational_url": "https://base-api-notice-management-api.app.cern.ch/getPolicy/https%3A%2F%2Fanother-community.org",
      "name": "Another community"
    },
    {
      "id": "https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl",
      "informational_url": "https://base-api-notice-management-api.app.cern.ch/getPolicy/https%3A%2F%2Foperations-portal.egi.eu%2Fvo%2Fview%2Fvoname%2Fxenon.biggrid.nl",
      "name": "Xenon biggrid"
    },
    {
      "id": "https://some-community.org",
      "informational_url": "https://base-api-notice-management-api.app.cern.ch/getPolicy/https%3A%2F%2Fsome-community.org",
      "name": "Some community"
    },
    {
      "id": "urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815",
      "informational_url": "https://base-api-notice-management-api.app.cern.ch/getPolicy/urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815",
      "name": "Nikhef"
    },
    {
      "id": "urn:idk:123456",
      "informational_url": "https://base-api-notice-management-api.app.cern.ch/getPolicy/urn:idk:123456",
      "name": "The community"
    },
    {
      "id": "urn:som:654321",
      "informational_url": "https://base-api-notice-management-api.app.cern.ch/getPolicy/urn:som:654321",
      "name": "Minimum info policy"
    }
  ]
}
```

## /getPolicy/\<uri\>
The endpoint `/getPolicy/<uri>` lists the information stored related to the requested uri.
One can only use a `GET` operation at this endpoint and most provide a valid uri. A valid uri is deemed to have the scheme `https`,`http` or `urn`.
If one does not provide a valid uri one would be presented with an error message stating the policy provided is invalid.

In the following example the uri presented was `operations-portal.egi.eu%2Fvo%2Fview%2Fvoname%2Fxenon.biggrid.nl` (notice the missing scheme).
```json
{
  "Not a valid policy": "operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl"
}
```
If one provides a valid uri, but it is not a known one, then the following could be presented"
```json
{
  "Not a policy id in db": "https://unknown.com"
}
```

Given that one has made a valid call to the endpoint the following information to the policy can be presented in json format.
- augment_policy_uris - list of policy uri's that are augmented by this policy
- aut - uri identifying the authority governing this policy
- aut_name - name of the authority, might contain a "#" to show the language code. Possible of multiple aut-name versions due to language difference
- contacts - a list of contact information holding the following values. If no contacts, then it's null
    - type - either `standard`, `security` or `privacy`
    - email - email of the contact
- description - a short description of the policy, might contain a "#" to show the language code. Possible of multiple description versions due to language difference
- id - string containing the URI of the identifier for the policy
- includes_policy_uris - list of policy uri's that are included in this policy and therefore implicitly fulfilled.
- notice_refresh_period - number of seconds after which this same notice has to be presented again to the same user
- policy_class - string from the limitative enumeration (‘purpose’, ‘acceptable-use’, ‘conditions’, ’sla’, ’privacy’). Possible to have a "#" to show jurisdiction, though only for policy_class type "privacy".
- policy_url - URL of the documentation of conditions and policies
- ttl - the time period (in seconds) after which this document should be retrieved again by consumers
- valid_from - time from which this policy is in effect

The following is an example of the response from a valid call to the endpoint. 
```json
{
  "policy": {
    "augment_policy_uris": [
      "https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl"
    ],
    "aut": "https://xenonexperiment.org/",
    "aut_name": "Xenon-nT collaboration",
    "aut_name#dk_DK": "Xenon-nT samarbejde",
    "contacts": [
      {
        "email": "research.support@somewhere.org",
        "type": "standard"
      },
      {
        "email": "secure@somewhere.org",
        "type": "security"
      },
      {
        "email": "safe@somewhere.org",
        "type": "privacy"
      }
    ],
    "description": "A community somwhere researching for the betterment of mankind (hopefully)",
    "description#dk_DK": "Et samarbejde et eller andet sted som forsker til fordel for menneskeheden (forhaabentlig)",
    "id": "https://some-community.org",
    "includes_policy_uris": [
      "urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815",
      "urn:idk:123456"
    ],
    "notice_refresh_period": 41212301,
    "policy_class": "privacy#eu",
    "policy_url": "https://some-community.org",
    "ttl": 21817600,
    "valid_from": "2025-10-17T09:00:00Z"
  }
}
```

## /
The endpoint `/` is the landing page. One can only use the `GET` operation and the endpoint is mainly a way to confirm that the instance is running. 
If working it should return "Hi, this is just a landing page". This also confirms that api's database connection was successfull. 


## /addPolicy
The endpoint is to add a policy to the policy registry. 
This is to be limited to users with clearance, hence the need for authentication. 
It supports only the `POST` operation and requires a valid token from the IDP containing the openid claim and the claim defined in the environment variables (`CLAIM_PATH=path_to_the_claim_in_token`). 

To add the policy one should provide it as a json object within the data of the `POST` request. 
The JSON should have the following structure: 
```
{
  "policy_entry": {
     ...
  },
  "policy": {
      ...
  }
}
```
The `policy_entry` json object needs to contain the following fields:
- name - a standard human readable name of the policy
- owner - the owner of the given policy, who is responsible for it, preferably an email

An example of the `policy_entry` json object could be the following:
```json
"policy_entry": {
    "name": "Global Science",
    "owner": "Esteban.Ocon@Haas.com"
}
```

The `policy` json object is similar to the `policy` object defined previously. 
There are a few changes though such as the authority names should be provided as a list with the parent object being `auth_languages`.
Within the list two fields needs to be provided for each item; `auth_name` and `language`. The `language` needs to be in accordance with [rfc4646](https://datatracker.ietf.org/doc/html/rfc4646).

An example of this could be:
```json
"auth_languages": [
      {
        "auth_name": "GlobalScience",
        "language": "en_US"
      },
      {
        "auth_name": "GlobalScience",
        "language": "fr_FR"
      }
]
```
This is similar for descriptions, as shown from the following example:
```json
    "descriptions": [
      {
        "description": "A collaborative international research organization.",
        "language": "en_US"
      },
      {
        "description": "Une organisation de recherche internationale collaborative.",
        "language": "fr_FR"
      }
    ]
```

Lastly, it needs to be mentioned that the optional `jurisdiction` to the `policy_class` is a seperate field that can be provided:
```
"policy": {
  ...
  "policy_jurisdiction": "EU",
  ...
}
```


The following is an example of a valid json object for the `/addPolicy` endpoint.
```json
{
  "policy_entry": {
    "name": "Global Science",
    "owner": "Esteban.Ocon@Haas.com"
  },
  "policy": {
    "augment_policy_uris": [
      "https://researchhub.org/document/8742"
    ],
    "aut": "https://global-science.org",
    "auth_languages": [
      {
        "auth_name": "GlobalScience",
        "language": "en_US"
      },
      {
        "auth_name": "GlobalScience",
        "language": "fr_FR"
      }
    ],
    "contacts": [
      {
        "email": "info@global-science.org",
        "type": "standard"
      },
      {
        "email": "support@global-science.org",
        "type": "security"
      }
    ],
    "descriptions": [
      {
        "description": "A collaborative international research organization.",
        "language": "en_US"
      },
      {
        "description": "Une organisation de recherche internationale collaborative.",
        "language": "fr_FR"
      }
    ],
    "id": "https://global-science.org/policy",
    "includes_policy_uris": [
      "https://partners.org/policies/v3/",
      "https://open-data.net/policies/aup/v2/"
    ],
    "notice_refresh_period": 2592000,
    "policy_class": "sla",
    "policy_jurisdiction": null,
    "policy_url": "https://global-science.org/policy",
    "ttl": 47304000,
    "valid_from": "2025-04-21 14:00:00"
  }
}
```


## /ui
This endpoint is the swagger ui. 
The swagger ui interface has been added to make it easier to navigate the endpoints and provides example values and calls to the various endpoints. 

### Main page
From here one is able to call the other endpoints endpoints of the api using the ui.

![Alt text](images/swagger_ui.jpg?raw=true "Title")

### Login
The login provides the option for users to obtain tokens. 
Tokens are necessary for the `/addPolicy` endpoint.
One can use an alternative method to obtain tokens as long as it is for the registered IDP and with the registered client. 
There are two different flows enabled pr. default from the api
- The implicit flow
- The authorization code flow

However, it must be mentioned that using the swagger ui with the authorization code flow is not advisable due to the fact that having the client secret in the front-end is not deemed safe. 
![Alt text](images/swagger_ui_login.jpg?raw=true "Title")

### Example of method
Below one can see an example of the information provided and available within the swagger ui when calling an endpoint. 
For the different endpoints are example data available (if needed) and curl examples should one want to use a terminal instead.

#### /
![Alt text](images/swagger_ui_landing.jpg?raw=true "Title")


#### /getPolicy
![Alt text](images/swagger_ui_get_policy.jpg?raw=true "Title")

