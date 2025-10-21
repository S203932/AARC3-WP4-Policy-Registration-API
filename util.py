'''
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>. 
'''
import logging
import os
import requests
from flask import Flask
from dotenv import load_dotenv
from authlib.oauth2.rfc7662 import IntrospectTokenValidator

def get_logger(name:str):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)-1s] [%(levelname)-1s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def get_env_variable(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and value is None:
        logger.error(f"Environment variable '{name}' is required, but not present.")
        raise RuntimeError(
            f"Environment variable '{name}' is required, but not present."
        )
    return value

realm_url = get_env_variable("IDP_REALM_URL", required=True)

class CustomIntrospectTokenValidator(IntrospectTokenValidator):
    """The following class is taken from the documentation: https://docs.authlib.org/en/latest/specs/rfc7662.html#use-introspection-in-resource-server"""
    def introspect_token(self,token_string):
        url = f'{realm_url}/protocol/openid-connect/token/introspect'
        data = {'token': token_string, 'token_type_hint': 'access_token'}
        auth = (get_env_variable("IDP_ID", required=True), get_env_variable("IDP_SECRET", required=True))
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        return resp.json()

class OAuthCache:

    def __init__(self, app: Flask) -> None:
        """Initialize the AuthCache."""
        self.app = app

    def delete(self, key: str) -> None:
        """
        Delete a cache entry.

        :param key: Unique identifier for the cache entry.
        """

    def get(self, key: str) -> str | None:
        """
        Retrieve a value from the cache.

        :param key: Unique identifier for the cache entry.
        :return: Retrieved value or None if not found or expired.
        """

    def set(self, key: str, value: str, expires: int | None = None) -> None:
        """
        Set a value in the cache with optional expiration.

        :param key: Unique identifier for the cache entry.
        :param value: Value to be stored.
        :param expires: Expiration time in seconds. Defaults to None (no expiration).
        """

load_dotenv()

logger = get_logger(__name__)

db_config = {
    "host": get_env_variable("DB_HOST", required=True),
    "user": get_env_variable("DB_USER", required=True),
    "password": get_env_variable("DB_PASSWORD", required=True),
    "port": int(get_env_variable("DB_PORT", required=True)),
    "database": get_env_variable("DB_NAME", required=True),
}

idp_config = {
    'name':'idp',
    'client_id': get_env_variable("IDP_ID", required=True),
    'client_secret':get_env_variable("IDP_SECRET", required=True),
    'access_token_url':f'{realm_url}/protocol/openid-connect/token',
    'authorize_url': f'{realm_url}/protocol/openid-connect/auth',
    'api_base_url': f'{realm_url}/protocol/openid-connect',
    'client_kwargs':{
        #'scope': 'openid email profile',
    }
}



""" idp_config = {
    'name':'idp',
    'client_id': get_env_variable("IDP_ID", required=True),
    'client_secret':get_env_variable("IDP_SECRET", required=True),
    'server_metadata_url':'https://auth.cern.ch/auth/realms/cern/.well-known/openid-configuration',
    'client_kwargs':{
        'scope': 'openid profile email',
    }
} """

app_secret = get_env_variable('SESSION_KEY', required=True)