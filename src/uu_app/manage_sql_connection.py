import logging
import keyring

from .yaml_interactor import fetch_yaml


logger = logging.getLogger(__name__)

def get_sql_credentials():
    config = fetch_yaml()
    connection_details = config['run_sql_scripts']['server_connection']
    password = keyring.get_password(connection_details["server"], connection_details["user"])
    if not password:
        new_password = input(f"No password for server: {connection_details['server']} username: {connection_details['user']}, Please enter password:")
        keyring.set_password(connection_details["server"], connection_details["user"], new_password)
        logger.warning(f"New password set for {connection_details["server"]} and user {connection_details["user"]}")
    connection_details['password'] = password
    logger.info(f"connection details returned for {connection_details["server"]} and user {connection_details["user"]}")
    return connection_details
