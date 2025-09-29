'''
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>. 
'''
import os
from dotenv import load_dotenv
import sqlparse
import mysql.connector
from util import get_logger

logger = get_logger(__name__)

def get_env_variable(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and value is None:
        logger.error(f"Environment variable '{name}' is required, but not present.")
        raise RuntimeError(
            f"Environment variable '{name}' is required, but not present."
        )
    return value


def init_db(connection_pool):
    file = open('initializationDB.sql', 'r')
    sql_db_init = file.read()
    file.close()
        
    commands = sqlparse.split(sql_db_init)

    conn = mysql.connector.connect(**db_config,autocommit=True)
    cursor = conn.cursor(dictionary=True)

    for command in commands:
        command = command.strip()
        
        if "REPLACE_BASE_FOR_UUID" in command:
            logger.info(f'Found a place to replace the base:{api_base} for actual uuid')
            command = str(command).replace("REPLACE_BASE_FOR_UUID",api_base)
            logger.info(f'The replaced command:{command}')

        if command:
            try:
                cursor.execute(command)
                logger.info(f'Following command succeded:{command[:30]}')
            except mysql.connector.errors.IntegrityError as err:
                logger.error(f"Failed duplicate command: {command[:30]}")        
    conn.close()


load_dotenv()

db_config = {
    "host": get_env_variable("DB_HOST", required=True),
    "user": get_env_variable("DB_USER", required=True),
    "password": get_env_variable("DB_PASSWORD", required=True),
    "port": int(get_env_variable("DB_PORT", required=True)),
    "database": get_env_variable("DB_NAME", required=True),
}

api_base = get_env_variable("APP_URL", required=True)
