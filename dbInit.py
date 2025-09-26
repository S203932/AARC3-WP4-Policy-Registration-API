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
    conn = connection_pool.get_connection()
    cursor = conn.cursor(dictionary=True)

    for command in commands:
        command = command.strip()
        
        if "REPLACE_BASE_FOR_UUID" in command:
            command.replace("REPLACE_BASE_FOR_UUID",api_base)

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

api_base = get_env_variable("API_NAME", required=True)
