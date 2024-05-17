import traceback
from typing import Tuple

from faker import Faker
from faker_airtravel import AirTravelProvider
from sqlalchemy import Engine, Inspector
from sqlalchemy import inspect

from config.database_info_class import DatabaseInfo
from config.db import create_engine_connection, create_database_connection
from ui.user_interface import main_user_interface
from util.database_utils import execute_sql_file


def initialize_engine(db_info: DatabaseInfo) -> Tuple[Engine, Inspector]:
    """
    Initializes the SQLAlchemy engine and inspector, and executes the DDL script.

    @param db_info: DatabaseInfo object containing the database connection information
    @return: Tuple containing the SQLAlchemy engine and inspector objects
    """

    # DDL Setting
    engine = create_engine_connection(db_info)
    execute_sql_file(engine, "models/airport-ddl.sql")

    # DB Connection Setting
    db_connection_engine = create_database_connection(db_info)
    inspector = inspect(db_connection_engine)
    return db_connection_engine, inspector


def initialize_lib() -> Faker:
    """
    Initializes and returns a Faker instance with the AirTravelProvider.

    @return: Faker instance with AirTravelProvider added
    """

    # Library Initialize
    fake = Faker()
    fake.add_provider(AirTravelProvider)
    return fake


def main() -> None:
    """
    Main function to initialize the database connection, Faker library, and run the main user interface.

    @return: None
    """
    try:
        # get dbinfo
        db_info = DatabaseInfo()
        db_connection_engine, inspector = initialize_engine(db_info)
        fake = initialize_lib()
        # RUN MAIN CODE
        main_user_interface(db_connection_engine, fake, inspector, db_info)
    except Exception as e:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()