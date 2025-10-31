"""
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>.
"""

import sqlparse
import mysql.connector
from util import get_logger, get_env_variable, db_config

logger = get_logger(__name__)

api_base = get_env_variable("APP_URL")


def init_db():
    file = open("initializationDB.sql", "r")
    sql_db_init = file.read()
    file.close()

    commands = sqlparse.split(sql_db_init)
    conn = mysql.connector.connect(**db_config, autocommit=True)
    cursor = conn.cursor(dictionary=True)

    for command in commands:
        command = command.strip()

        if "REPLACE_BASE_FOR_ID" in command:
            logger.info(f"Found a place to replace the base:{api_base} for actual id")
            command = str(command).replace("REPLACE_BASE_FOR_ID", api_base)
            logger.info(f"The replaced command:{command}")

        if command:
            try:
                cursor.execute(command)
                logger.info(f"Following command succeded:{command[:30]}")
            except mysql.connector.errors.IntegrityError as err:
                logger.error(f"Failed duplicate command: {command[:30]}")
    conn.close()


# Init the database and populate
if __name__ == "__main__":
    init_db()
