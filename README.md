# AARC3-WP4-Policy-Registration-API
This is a base implementation of a policy registry API in accordance with AARC-G083

# Requirements to run the api
- A database that runs a mysql database called `aup`

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
- One can use docker compose  given that one populates the `.env` first with the database information. 
- Alternatively, one provide the db at runtime.

# Structure of the aup database
![Alt text](API_DB_class.jpg?raw=true "Title")
