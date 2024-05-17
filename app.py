from faker import Faker
from faker_airtravel import AirTravelProvider
from sqlalchemy import inspect

from config.db import create_engine_connection, create_database_connection
from config.database_info_class import DatabaseInfo
from ui.user_interface import main_user_interface
from util.database_utils import execute_sql_file
import traceback


def initialize_engine(db_info: DatabaseInfo):
    # DDL Setting
    engine = create_engine_connection(db_info)
    execute_sql_file(engine, "models/airport-ddl.sql")
    # DB Connection Setting
    db_connection_engine = create_database_connection(db_info)
    inspector = inspect(db_connection_engine)
    return db_connection_engine, inspector


def initialize_lib():
    # Library Initialize
    fake = Faker()
    fake.add_provider(AirTravelProvider)
    return fake


def main():
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