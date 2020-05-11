"""
Description: This module is written to interface with databases.

Title: database_interface.py

Author: theStygianArchitect
"""
import sys
from typing import Dict
from typing import Text
from typing import Optional

try:
    import pandas
    from pydantic import BaseModel  # pylint: disable=E0611
    from pytds.login import NtlmAuth
    from sqlalchemy import create_engine
except ModuleNotFoundError as module_not_found_error:
    print(module_not_found_error)
    print('Please install required packages.')
    sys.exit()


class DatabaseInformation(BaseModel):  # pylint: disable=R0903
    """Develop Database Information model."""

    server_fqdn: Text
    instance_name: Optional[Text] = None
    port: Optional[int] = None
    logon_domain: Optional[Text] = None
    database_name: Text
    user_name: Text
    user_pass: Text


def mssql_database_connection(database_information: DatabaseInformation,
                              windows_authentication: bool = False,
                              connection_arguments: Dict = None):
    """Create MSSQL database connection.

    This function will create a sql database connection. This function
    will support both windows and sql authentication specified by the
    windows_authentication variable. The driver used to handle database
    communication is python-tds.

    Notes:
        connection_arguments should map to python-tds arguments.

    Args:
        database_information(DatabaseInformation): A key, value object
            containing the database connection information.
        windows_authentication(bool): Deciding variable to determine
            the type of authentication to use.
        connection_arguments(Dict): A key, value object containing
            arguments passed to the engine.

    Returns:
        The database connection object.

    """
    server_name = database_information.server_fqdn
    database_name = database_information.database_name
    user_name = database_information.user_name
    user_pass = database_information.user_pass

    if windows_authentication:
        if not database_information.instance_name:
            connection_string = f"mssql+pytds://{server_name}/{database_name}"
        else:
            instance_name = database_information.instance_name
            connection_string = f"mssql+pytds://{server_name}\\{instance_name}/{database_name}"

        user_name = f"{database_information.logon_domain}\\{user_name}"
        if connection_arguments is None:
            connection_arguments = {}
        if 'auth' not in connection_arguments:
            connection_arguments['auth'] = NtlmAuth(user_name, user_pass)
    else:
        if not database_information.instance_name:
            connection_string = f"mssql+pytds://{user_name}:{user_pass}@{server_name}/" \
                                f"{database_name}"
        else:
            instance_name = database_information.instance_name
            connection_string = f"mssql+pytds://{user_name}:{user_pass}@{server_name}\\" \
                                f"{instance_name}/{database_name}"
    engine = create_engine(connection_string, connect_args=connection_arguments)
    return engine


def postgres_database_connection(database_information: DatabaseInformation,
                                 connection_arguments: Dict = None):
    """Create PostgreSQL database connection.

    This function will create a sql database connection. The driver
    used to handle database communication is psycopg2.

    Notes:
        connection_arguments should map to psycopg2 arguments.

    Args:
        database_information(DatabaseInformation): A key, value object
            containing the database connection information.
        connection_arguments(Dict): A key, value object containing
            arguments passed to the engine.

    Returns:
        The database connection object.

    """
    server_name = database_information.server_fqdn
    database_name = database_information.database_name
    user_name = database_information.user_name
    user_pass = database_information.user_pass
    port = database_information.port

    connection_string = f"postgresql+psycopg2://{user_name}:{user_pass}@{server_name}:{port}/" \
                        f"{database_name}"
    engine = create_engine(connection_string, connect_args=connection_arguments)
    return engine


def mysql_database_connection(database_information: DatabaseInformation,
                              connection_arguments: Dict = None):
    """Create MySQL database connection.

    This function will create a sql database connection. The driver
    used to handle database communication is pymysql.

    Notes:
        connection_arguments should map to pymysql arguments.

    Args:
        database_information(DatabaseInformation): A key, value object
            containing the database connection information.
        connection_arguments(Dict): A key, value object containing
            arguments passed to the engine.

    Returns:
        The database connection object.

    """
    server_name = database_information.server_fqdn
    database_name = database_information.database_name
    user_name = database_information.user_name
    user_pass = database_information.user_pass

    connection_string = f"mysql+pymysql://{user_name}:{user_pass}@{server_name}/{database_name}"
    engine = create_engine(connection_string, connect_args=connection_arguments)
    return engine


def query_mssql_server(database_information: DatabaseInformation, sql_command: Text,
                       windows_authentication: bool = False,
                       connection_arguments: Dict = None) -> pandas.Dataframe:
    """Query MSSQL database.

    This function will create a MSSQL database connection. This
    function will support both windows and sql authentication specified
    by the windows_authentication variable.

    Args:
        database_information(DatabaseInformation): A key, value object
            containing the database connection information.
        sql_command(Text): The sql query that's ran against the
            database.
        windows_authentication(bool): Deciding variable to determine
            the type of authentication to use.
        connection_arguments(Dict): A key, value object containing
            arguments passed to the engine.

    Returns:
        The database connection object.

    """
    engine = mssql_database_connection(database_information, windows_authentication,
                                       connection_arguments)
    data_frame = pandas.read_sql(sql_command, engine)
    return data_frame


def query_postgresql_server(database_information: DatabaseInformation, sql_command: Text,
                            connection_arguments: Dict = None) -> pandas.Dataframe:
    """Query PostgreSQL database.

    This function will create a PostgreSQL database connection.

    Args:
        database_information(DatabaseInformation): A key, value object
            containing the database connection information.
        sql_command(Text): The sql query that's ran against the
            database.
        connection_arguments(Dict): A key, value object containing
            arguments passed to the engine.

    Returns:
        The database connection object.

    """
    engine = postgres_database_connection(database_information, connection_arguments)
    data_frame = pandas.read_sql(sql_command, engine)
    return data_frame


def query_mysql_server(database_information: DatabaseInformation, sql_command: Text,
                       connection_arguments: Dict = None) -> pandas.Dataframe:
    """Query MySQL database.

    This function will create a MySQL database connection.

    Args:
        database_information(DatabaseInformation): A key, value object
            containing the database connection information.
        sql_command(Text): The sql query that's ran against the
            database.
        connection_arguments(Dict): A key, value object containing
            arguments passed to the engine.

    Returns:
        The database connection object.

    """
    engine = mysql_database_connection(database_information, connection_arguments)
    data_frame = pandas.read_sql(sql_command, engine)
    return data_frame
