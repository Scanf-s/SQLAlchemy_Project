import re
from typing import List, Dict, Any, Union

from faker import Faker
from sqlalchemy import delete, text, Inspector
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.schema import CreateTable, MetaData
from sqlalchemy.schema import Table, Column

from config.DatabaseInfo import DatabaseInfo
from util.dummy_generators import generate_data_with_type
from util.error.error_handler import exception_handler


@exception_handler
def print_table(engine: Engine, table_name: str) -> list[dict]:
    """
    Executes a SQL query using the SQLAlchemy engine to fetch and print all data from the specified table.

    :param engine: SQLAlchemy engine object connected to the target database
    :param table_name: Name of the database table to query
    :raises Exception: Any exceptions raised during the execution are handled by the exception handler
    """
    with engine.connect() as connection:
        sql = text("SELECT * FROM " + table_name)
        result = connection.execute(sql)
        conv_result = [dict(row) for row in result.mappings()]
        return conv_result



@exception_handler
def delete_current_data(connection: Connection, table: Table) -> None:
    """
    Deletes all data from the specified table using SQLAlchemy.

    @param connection: SQLAlchemy connection object (e.g., from with engine.connect() as connection:)
    @param table: SQLAlchemy Table object representing the table to delete data from
    @raise Exception: Any exceptions raised during the execution are handled by the exception handler
    """

    connection.execute(delete(table))
    connection.commit()


@exception_handler
def get_table_metadata(engine: Engine, table_name: Union[str, Table]) -> Table:
    """
    Retrieves metadata for the specified table from the MySQL database.

    @param engine: SQLAlchemy engine object connected to the target database
    @param table_name: Name of the table as a string
    @return: SQLAlchemy Table object containing the table's metadata
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    return table


@exception_handler
def get_all_tables_from_database(engine: Engine) -> List[Table]:
    """
    Retrieves all table metadata from the MySQL database schema specified in the engine.

    @param engine: SQLAlchemy engine object connected to the target database
    @return: List of SQLAlchemy Table objects
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    all_tables = list(metadata.tables)
    return all_tables


@exception_handler
def insert_into_all_tables(engine, dummy_data: Dict) -> None:
    """
    Inserts data into all specified tables using SQLAlchemy.

    @param engine: SQLAlchemy engine object connected to the target database
    @param dummy_data: Dictionary where keys are table names and values are lists of dictionaries containing dummy data
    @param mode: Operation mode; 'y' to delete existing data before insertion, 'n' to keep existing data
    """
    with engine.connect() as connection:
        for table_name in dummy_data.keys():
            table_metadata = get_table_metadata(engine, table_name)
            connection.execute(table_metadata.insert(), dummy_data[table_name])
            connection.commit()


@exception_handler
def insert_dummy_data(engine, table_name: str, dummy_data: List[Dict], mode: str) -> None:
    """
    Inserts generated dummy data into the specified table.

    @param engine: SQLAlchemy engine object connected to the target database
    @param table_name: Name of the table as a string
    @param dummy_data: List of dictionaries containing the dummy data to be inserted
    @param mode: Operation mode; 'y' to delete existing data before insertion, 'n' to keep existing data
    """
    # DB에서 테이블 원형 가져오기
    table = get_table_metadata(engine, table_name)

    with engine.connect() as connection:
        # DELETE
        if mode == 'y' or mode == 'Y':
            delete_current_data(connection, table)

        # INSERT INTO
        for data in dummy_data:
            connection.execute(table.insert().values(data))
        connection.commit()


@exception_handler
def get_column_type_detail(table: Table, column: Column) -> Dict[str, Any]:
    """
    Retrieves detailed column type information for a specific column in a table.

    @param table: SQLAlchemy Table object containing the column
    @param column: SQLAlchemy Column object for which to retrieve detailed information
    @return: Dictionary containing detailed information about the column. The dictionary keys are:
             'table_name', 'col_name', 'type', 'size', 'decimal_place', 'enum_values', 'primary', 'unique'.
             - 'type' is the data type (e.g., VARCHAR, INT)
             - 'size' is the size of the data type (e.g., 255 for VARCHAR(255))
             - 'decimal_place' is the number of decimal places (for NUMERIC types)
             - 'enum_values' is a list of possible values for ENUM types
             - 'primary' is 'True' if the column is a primary key
             - 'unique' is 'True' if the column has a unique constraint
    """
    column_type = column.type
    pattern = r"(\w+)\s*(\((\d+)(,\s*(\d+))?\))?(?:\s*CHARACTER SET \w+)?(?:\s*COLLATE \w+)?"  # 정규식 (CHAT-GPT 사용)
    matches = re.findall(pattern, str(column_type))
    type_detail = {
        'table_name': table.name,
        'col_name': column.name,
        'type': None,
        'size': None,
        'decimal_place': None,
        'enum_values': None,
        'primary': None,
        'unique': None
    }

    if matches:
        col_type, col_size, decimal_place = matches[0][0], matches[0][2], matches[0][4]
        type_detail['type'] = col_type
        type_detail['size'] = int(col_size) if col_size else None
        type_detail['decimal_place'] = int(decimal_place) if decimal_place else None

    # primary
    if column.primary_key:
        type_detail['primary'] = 'True'

    # 유니크 속성 확인
    for index in table.indexes:
        if index.unique and column.name in index.columns:
            type_detail['unique'] = 'True'
            break

    # ENUM 값 뽑아오기
    if str(column_type) == "ENUM":
        type_detail['enum_values'] = column_type.enums

    return type_detail


def create_all_dummy_helper(fake: Faker, table: Table, n: int) -> List[Dict]:
    """
    Generates dummy data for the specified table.

    @param fake: Faker object used to generate fake data
    @param table: SQLAlchemy Table object for which to generate dummy data
    @param n: Number of dummy data entries to generate
    @return: List of dictionaries, each containing dummy data for a table row
    """
    dummy_data = []
    check_str_duplicate = set()
    check_num_duplicate = set()
    for i in range(n):
        # n개의 더미 데이터 생성
        data_row = {}
        for column in table.columns:
            if str(column.autoincrement) == "True":
                continue
            type_detail = get_column_type_detail(table, column)  # 해당 column의 상세정보를 dictionary 형태로 가져와줌
            data_row[column.name] = generate_data_with_type(fake, type_detail, check_str_duplicate, check_num_duplicate)  # Row 하나씩 더미데이터 생성해줌
        dummy_data.append(data_row)  # 리스트에 저장

    return dummy_data


def create_all_dummy(engine: Engine, fake: Faker, n: int, mode: str):
    """
    Retrieves metadata for all tables using get_all_tables_from_database(), generates dummy data for each table,
    stores the data in a dictionary, and passes it to insert_into_all_tables() for insertion.

    @param engine: SQLAlchemy engine object connected to the target database
    @param fake: Faker object used to generate fake data
    @param n: Number of dummy data entries to generate per table
    @param mode: Operation mode; 'y' to delete existing data before insertion, 'n' to keep existing data
    """
    table_list = get_all_tables_from_database(engine)
    all_dummy_data = {}

    if mode == 'y' or mode == 'Y':
        with engine.connect() as connection:
            for table in table_list:
                table_metadata = get_table_metadata(engine, table)
                delete_current_data(connection, table_metadata)
            connection.commit()

    for table in table_list:
        table_metadata = get_table_metadata(engine, table)
        generated_data = create_all_dummy_helper(fake, table_metadata, n)
        all_dummy_data[table_metadata.name] = generated_data

    insert_into_all_tables(engine, all_dummy_data)


@exception_handler
def is_column_primary_key(engine: Engine, table_name: str, col_name: str) -> bool:
    """
    Checks if a specific column in a given table is a primary key.

    @param engine: SQLAlchemy engine object connected to the target database
    @param table_name: Name of the table containing the column
    @param col_name: Name of the column to check
    @return: True if the column is a primary key, False otherwise
    """
    meta_table = get_table_metadata(engine, table_name)
    for column in meta_table.columns:
        if col_name == column.name:
            return column.primary_key
    return False


@exception_handler
def make_column_details_dictionary(engine: Engine, inspector: Inspector, table_name: str, db_info: DatabaseInfo):
    """
    Retrieves column details for a specified table and stores them in a dictionary.

    @param engine: SQLAlchemy engine object connected to the target database
    @param inspector: SQLAlchemy Inspector object for reflecting database metadata
    @param table_name: Name of the table for which to retrieve column details
    @param db_info: Database information object containing database name
    @return: Dictionary with table name as key and list of column details as value
    """
    temp_dict = {}
    columns = inspector.get_columns(table_name, db_info.database_name)
    column_dictionary_list = []
    for column in columns:
        column_details = {
            'name': column['name'],
            'type': str(column['type']),
            'primary': is_column_primary_key(engine, table_name, column['name']),
            'comment': column['comment'],
            'default': column['default'],
            'nullable': column['nullable'],
            'autoincrement': column.get('autoincrement')
        }
        column_dictionary_list.append(column_details)
    temp_dict[table_name] = column_dictionary_list
    return temp_dict


@exception_handler
def get_ddl_script(engine: Engine, table_name: str):
    """
    Prompts the user for a table name and prints the DDL script for the specified table.
    https://stackoverflow.com/questions/64677402/get-ddl-from-existing-databases-sqlalchemy

    @param table_name:
    @param engine: SQLAlchemy engine object connected to the target database
    @raise ValueError: if table name is not exists in database schema
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)

    if table_name in metadata.tables.keys():
        table_metadata = metadata.tables[table_name]
        return CreateTable(table_metadata).compile(engine)
    else:
        raise ValueError


@exception_handler
def get_view_list_details(engine: Engine, inspector: Inspector, db_info: DatabaseInfo) -> Dict[str, List]:
    """
    Retrieves details of all views in the specified database and returns a dictionary with view names as keys
    and lists of column details as values.

    @param engine: SQLAlchemy engine object connected to the target database
    @param inspector: SQLAlchemy Inspector object for reflecting database metadata
    @param db_info: DatabaseInfo object containing the database name
    @return: Dictionary with view names as keys and lists of column details as values
    """
    result = {}
    for view_name in inspector.get_view_names(db_info.database_name):
        view_definition = inspector.get_view_definition(view_name)
        re_aliases = re.findall(r'AS\s+`(\w+)`', view_definition)  # 'as'로 alias된 이름 검사
        re_table_name = re.findall(r'FROM\s+`(\w+)`', view_definition, re.IGNORECASE)  # 테이블 이름 검사

        if not re_table_name:
            continue

        table_name = re_table_name[0]
        columns = inspector.get_columns(table_name, db_info.database_name)

        column_dictionary_list = []
        for column in columns:
            if column['name'] in re_aliases:
                column_details = {
                    'name': column['name'],
                    'type': str(column['type']),
                    'primary': is_column_primary_key(engine, table_name, column['name']),
                    'comment': column['comment'],
                    'default': column['default'],
                    'nullable': column['nullable'],
                    'autoincrement': column.get('autoincrement')
                }
                column_dictionary_list.append(column_details)
        result[view_name] = column_dictionary_list

    return result


# @exception_handler
# def create_mysql_view(engine: Engine, inspector: Inspector, table_metadata: Table, db_info: DatabaseInfo) -> None:
#     """
#     Creates a view in the specified MySQL database based on the user-provided table and column selections.
#
#     @param engine: SQLAlchemy engine object connected to the target database
#     @param inspector: SQLAlchemy Inspector object for reflecting database metadata
#     @param table_metadata: SQLAlchemy Table object containing metadata of the base table
#     @param db_info: DatabaseInfo object containing the database connection information
#     @return: None
#     """
#
#     view_target_column_list = []
#     view_name = input("생성할 View 이름을 입력하세요 : ")
#     print(f"Table {table_metadata.name}에 있는 Column 명은 다음과 같습니다.")
#     column_name_list = get_column_names(inspector, table_metadata.name, db_info)
#     print(column_name_list)
#
#     while True:
#         column_name = input("View에 추가할 Column name을 입력해주세요. 'quit'을 입력하면 종료합니다 >>> ")
#         if column_name == 'quit':
#             break
#         elif column_name in column_name_list:
#             view_target_column_list.append(column_name)
#         else:
#             print("잘못된 컬럼 명을 입력했습니다. 상단에 출력된 컬럼 명만 입력해 주세요.")
#
#     columns_str = ", ".join(view_target_column_list)
#     view_statement = f"CREATE VIEW {view_name} AS SELECT {columns_str} FROM {table_metadata.name}"
#
#     with engine.connect() as connection:
#         connection.execute(text(view_statement))
#         connection.commit()
#         print(f"{view_name} 생성 성공")

# @exception_handler
# def get_column_names(inspector: Inspector, table_name: str, db_info: DatabaseInfo) -> List:
#     """
#     Retrieves the names of all columns in the specified table.
#
#     @param inspector: SQLAlchemy Inspector object for reflecting database metadata
#     @param table_name: The name of the table from which to retrieve column names
#     @param db_info: DatabaseInfo object containing the database name
#     @return: List of column names in the specified table
#     """
#
#     columns = inspector.get_columns(table_name, db_info.database_name)
#     return [column['name'] for column in columns]

# @exception_handler
# def execute_sql_file(engine: Engine, file_path: str) -> None:
#     """
#     Executes the SQL commands contained in a file.
#
#     :param engine: SQLAlchemy engine object created using create_engine()
#     :param file_path: Path to the SQL file containing the commands to execute
#     """
#     with open(file_path, 'r', encoding='utf-8') as file:
#         sql_commands = file.read()
#     with engine.connect() as connection:
#         for command in sql_commands.split(';'):
#             command = command.strip()
#             if command:
#                 connection.execute(text(command))
