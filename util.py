"""
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import os
import yaml
import requests
import base64
import json
import re
from authlib.oauth2.rfc7662 import IntrospectTokenValidator


def get_logger(name: str):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(name)-1s] [%(levelname)-1s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def get_env_variable(name, default=None):
    value = os.getenv(name, default)
    if value is None:
        logger.error(f"Environment variable '{name}' is required, but not present.")
        raise RuntimeError(
            f"Environment variable '{name}' is required, but not present."
        )
    return value

def load_api_spec():
    """Load openapi.yaml and replace ${VAR} placeholders with environment values."""
    spec_path = os.path.join(os.path.dirname(__file__), "openapi.yaml")
    with open(spec_path, "r") as f:
        raw_yaml = f.read()

    # Replace ${VAR_NAME} with the corresponding environment variable
    def replace_env_var(match):
        var_name = match.group(1)
        value = os.getenv(var_name)
        if value is None:
            raise RuntimeError(f"Environment variable '{var_name}' not set but required by openapi.yaml")
        return value

    # Perform replacement
    pattern = re.compile(r"\$\{([^}^{]+)\}")
    resolved_yaml = pattern.sub(replace_env_var, raw_yaml)

    # Load the modified YAML into a Python dict
    spec = yaml.safe_load(resolved_yaml)

    return spec


class CustomIntrospectTokenValidator(IntrospectTokenValidator):
    """The following class is taken from the documentation: https://docs.authlib.org/en/latest/specs/rfc7662.html#use-introspection-in-resource-server"""

    def __init__(self):
        self.claim = get_env_variable("CLAIM_PATH")
        self.id = get_env_variable("IDP_ID")

    def introspect_token(self, token_string):
        url = get_env_variable("IDP_INTROSPECTION_ENDPOINT")
        data = {"token": token_string, "token_type_hint": "access_token"}
        auth = (self.id, get_env_variable("IDP_SECRET"))
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        return resp.json()

    def validate_aud(self,token):
        logger.info(f'aud from info:{token.get("aud")}')
        if not token.get("aud", self.id):
            return False
        else:
            return True

    def validate_claim(self,token_string):

        # Decoding the content of the token
        content = token_string.split(".")
        # Padding with = to acheive proper length
        content[1] += "=" * (-len(content[1]) % 4)
        decoded_bytes = base64.urlsafe_b64decode(content[1])
        content = json.loads(decoded_bytes)
        logger.info(f'The content after decoding:{content}')

        # Checking if the claim is in the token 
        claims = self.claim.strip("/").split("/")
        current = content

        for claim in claims:
            if isinstance(current, dict):
                if claim not in current:
                    return False
                else:
                    current = current[claim]
            elif isinstance(current, list):
                if claim in current:
                    return True
                else:
                    return False
            else:
                return False


db_config = {
    "host": get_env_variable("DB_HOST"),
    "user": get_env_variable("DB_USER"),
    "password": get_env_variable("DB_PASSWORD"),
    "port": int(get_env_variable("DB_PORT")),
    "database": get_env_variable("DB_NAME"),
}


logger = get_logger(__name__)

api_base = get_env_variable("APP_URL")

app_base = get_env_variable("APP_BASE")
