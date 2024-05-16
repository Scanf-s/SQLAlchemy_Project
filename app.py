from faker import Faker
from faker_airtravel import AirTravelProvider
from sqlalchemy import inspect

from config.db import create_engine_connection, create_database_connection
from config.db_info import DatabaseInfo
from ui.user_interface import main_user_interface
from util.database_utils import execute_sql_file

if __name__ == "__main__":
    # get dbinfo
    db_info = DatabaseInfo()

    # DDL Setting
    engine = create_engine_connection(db_info)
    execute_sql_file(engine, "models/airport-ddl.sql")

    # DB Connection Setting
    db_connection_engine = create_database_connection(db_info)
    inspector = inspect(db_connection_engine)

    # Library Initialize
    fake = Faker()
    fake.add_provider(AirTravelProvider)

    # RUN MAIN CODE
    main_user_interface(db_connection_engine, fake, inspector, db_info)
