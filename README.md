# AARC3-WP4-Policy-Registration-API
This is a base implementation of a policy registry API in accordance with AARC-G083

# Requirements to run the api
- A mysql database that has the following structure as seen below.

## Structure of the aup database
![Alt text](API_DB_class.jpg?raw=true "Title")

# How to run the api
There are different ways to run the api. True for all of them is that one needs to provide the database information to the api. 
The database information that needs to be provided are the following:
- `DB_HOST=the_AARC_DB`
- `DB_USER=the_AARC_User`
- `DB_PASSWORD=the_AARC_User_Password`
- `DB_PORT=the_AARC_DB_Port`
- `DB_NAME=name_of_the_database`

These are the following ways to run the api.

## Docker image
- Pull the newest image from the [Packages](https://github.com/S203932/AARC3-WP4-Policy-Registration-API/pkgs/container/aarc3-wp4-policy-registration-api%2Fmyapp)
- When deploying the image on kubernetes or your given platform, provide the aformentioned database information.

## Docker file
- One can use docker compose given that one populates the `.env` first with the database information. 
- Alternatively, one provide the db information at runtime.

# Api Endpoints
The following are the available endpoints of the api. 

## /getPolicies
The endpoint `/getPolicies` presents a list of all the available policies in json format.
One can only use a `GET` operation at this endpoint.
For each policy one will be presented with the `name`, `uri` and `information_url`.
- name - the name of the policy
- uri - a 36 character uuid. It is a unique identifier for the policy within the instance.
- information_url - a link to get further information about the given policy from the api. The link is `/getPolicy/<uri>`.

The following is an example of policies returned from the given endpoint.
```json
{
  "policies": [
    {
      "informational_url": "https://policy-api.org/getPolicy/4a6d33b3-34c0-4d39-9c87-f39d6f932a6b",
      "name": "AARC documentation example2",
      "uri": "4a6d33b3-34c0-4d39-9c87-f39d6f932a6b"
    },
    {
      "informational_url": "https://policy-api.org/getPolicy/8eaa6f4e-bf42-4cb4-8048-e26864c7ec58",
      "name": "AARC documentation example",
      "uri": "8eaa6f4e-bf42-4cb4-8048-e26864c7ec58"
    }
  ]
}
```

## /getPolicy/\<uri\>
The endpoint `/getPolicy/<uri>` lists the information stored related to the requested uri.
One can only use a `GET` operation at this endpoint and most provide a valid uri, i.e. a 36 character uuid.
If one does not provide a valid uri, in this example the uri presented was `4d6fewf33bqd3-34c0-4d39-9c87-f39d6f932a6dd`,then the follwing message will be displayed.
```json
{
  "Not uuid": "4d6fewf33bqd3-34c0-4d39-9c87-f39d6f932a6dd"
}
```

Given that one has made a valid call to the endpoint the following information to the policy can be presented in json format.
- uri - the uuid of the policy within the instance
- description - a short description of the policy
- policy_url - URL of the documentation of conditions and policies
- auth - URI identifying the authority governing this policy
- valid_from - time from which this policy is in effect
- ttl - the time period after which this document should be retrieved again by consumers
- policy_class - string from the limitative enumeration (‘purpose’, ‘acceptable-use’, ‘conditions’, ’sla’, ’privacy’)
- notice_refresh_period - number of seconds after which this same notice has to be presented again to the same user
- id - string containing the URI of the identifier for the policy
- auth_name - name of the authority
- contacts - a list of contact information holding the following values. If no contacts, then it's null
    - type - either `standard`, `security` or `privacy`
    - email - email of the contact
- includes_policy_uris - list of policy uri's that are included in this policy and therefore implicitly fulfilled.
- augment_policy_uris - list of policy uri's that are augmented by this policy, e.g. the WISE Baseline AUP itself

The following is an example of a valid call to the endpoint. 
```json
{
  "policy": {
    "augment_policy_uris": [
      "https://wise-community.org/wise-baseline-aup/v1/"
    ],
    "auth": "https://xenonexperiment.org/",
    "auth_name": "Xenon-nT collaboration",
    "contacts": [
      {
        "email": "grid.support@nikhef.nl",
        "type": "standard"
      },
      {
        "email": "vo-xenon-admins@biggrid.nl",
        "type": "security"
      }
    ],
    "description": "detector construction and experiment analysis for the search of dark matter using Xenon detectors",
    "id": "https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl",
    "includes_policy_uris": null,
    "notice_refresh_period": null,
    "policy_class": "purpose",
    "policy_url": "https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl",
    "ttl": 31557600,
    "uri": "4a6d33b3-34c0-4d39-9c87-f39d6f932a6b",
    "valid_from": "Fri, 29 Jul 2011 00:00:00 GMT"
  }
}
```

## /
The endpoint `/` is the landing page. One can only use the `GET` operation and the endpoint is mainly a way to confirm that the instance is running. 
If working it should return "Hi, this is just a landing page".


## /addPolicy/\<policy\>
The endpoint has no function and is a work in progress. 
It supports only the `POST` operation. 
If one tries to access it with the `policy` called `somePolicy`, then it should return:
```json
{
  "data": "Attempt to add somePolicy"
}
```
The endpoint does not prompt any interaction with the database, nor stores any information given. 
