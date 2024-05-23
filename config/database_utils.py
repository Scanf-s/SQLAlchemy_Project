from sqlalchemy import create_engine, Engine
from util.error.error_handler import exception_handler
from .DatabaseInfo import DatabaseInfo


@exception_handler
def create_engine_connection(db_info: DatabaseInfo) -> Engine:
    """
    Creates a connection engine for MySQL initialization.

    @param db_info: DatabaseInfo object containing the database connection information
    @return: Successfully created SQLAlchemy engine object
    @raise Exception: Raises an exception if there is an error in creating the connection
    """

    engine_connection_string = (
        f'{db_info.database}://root:123123@'
        f'{db_info.address}:{db_info.port}'
    )
    engine = create_engine(
        engine_connection_string,
        echo=False
    )
    return engine


@exception_handler
def create_database_connection(db_info: DatabaseInfo) -> Engine:
    """
    Creates a connection engine for connecting to a MySQL database.

    This function uses SQLAlchemy's create_engine function to create an engine
    for connecting to a MySQL database. If the connection fails, it prints an error message.

    @param db_info: DatabaseInfo object containing the database connection information
    @return: Successfully created SQLAlchemy engine object
    @raise Exception: Raises an exception if there is an error in creating the connection
    """
    database_connection_string = (
        f'{db_info.database}://{db_info.username}:{db_info.password}@'
        f'{db_info.address}:{db_info.port}/{db_info.database_name}?'
        f'charset={db_info.charset}'
    )

    engine = create_engine(
        database_connection_string,
        echo=False
    )
    return engine
