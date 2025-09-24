
import os
from dotenv import load_dotenv
import sqlparse

def get_env_variable(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and value is None:
        raise RuntimeError(
            f"Environment variable '{name}' is required, but not present."
        )
    return value


def init_db(connection_pool):
    file = open('initializationDB.sql', 'r')
    sql_db_init = file.read()
    file.close()
        
    commands = sqlparse.split(sql_db_init)

    for command in commands:
        command = command.strip()
        if command:
            try:
                conn = connection_pool.get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute(command)
                conn.close()
            except mysql.connector.Error as err:
                print(f"Error:{err}")
                print(f"Failed command: {command[:30]}")


load_dotenv()

db_config = {
    "host": get_env_variable("DB_HOST", required=True),
    "user": get_env_variable("DB_USER", required=True),
    "password": get_env_variable("DB_PASSWORD", required=True),
    "port": int(get_env_variable("DB_PORT", required=True)),
    "database": get_env_variable("DB_NAME", required=True),
}