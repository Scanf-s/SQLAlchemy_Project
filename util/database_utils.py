import re

from sqlalchemy import delete, text, Inspector
from sqlalchemy.schema import CreateTable, MetaData

from config.database_info_class import DatabaseInfo
from util.dummy_generators import generate_data_at_once
from util.error.error_handler import exception_handler
from util.utils import table_mapper

from sqlalchemy.schema import Table
from typing import List, Dict, Any


@exception_handler
def execute_sql_file(engine, file_path: str) -> None:
    """
    models/airport-ddl.sql을 실행해주는 함수

    @param engine: sqlalchemy의 create_engine()에서 생성된 engine
    @param file_path: ddl 파일 경로
    """
    with open(file_path, 'r', encoding='utf-8') as file:  # file_path에서 read only, 선택한 encoding으로 파일 열기
        sql_commands = file.read()  # 파일 전체를 읽어서, sql_commands 객체가 built-in function인 open이 읽은 내용을 가리키게됨
    with engine.connect() as connection:
        for command in sql_commands.split(';'):  # SQL Query는 모두 ';'단위로 실행하므로 ';'로 split해서 리스트에 저장
            command = command.strip()  # command 양옆에 존재하는 공백 싹다 삭제해야 정상적으로 작동
            if command:
                connection.execute(text(command))  # string type command를 text로 변환해서 쿼리 실행


@exception_handler
def print_table(engine, table_name: str) -> None:
    """
    SQLAlchemy 엔진 객체와 테이블 이름을 사용하여 SQL 쿼리를 실행하고,
    결과를 콘솔에 출력해준다. 함수는 데이터베이스 연결을 관리하며, SELECT 쿼리를 통해
    테이블의 모든 데이터를 검색한다.

    @param engine: SQLAlchemy 엔진 객체
    @param table_name: 조회할 데이터베이스 테이블의 이름입니다.
    @raise Exception: 함수 호출 시, Exception을 처리해야 한다.
    """
    with engine.connect() as connection:
        sql = text("SELECT * FROM " + table_name)
        result = connection.execute(sql)
        # execute() -> returns CursorResult that a sequence of Row objects.
        conv_result = result.mappings().all()
        # mappings() -> returns MappingResult
        # MappingResult.all() -> returns sequence[Rowmapping] array
        # Rowmapping -> dictionary
        # 따라서 conv_result에는 dictionary가 담기고, for문으로 돌릴 수 있음
        print(f'\n<<<<<<<<<<<<<<<<<<<<<<<<<<< {table_name} 더미데이터 내역 >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        for dic in conv_result:
            print(dic)


@exception_handler
def delete_current_data(connection, table: Table) -> None:
    """
    SQLAlchemy를 통해 table을 삭제해주는 함수.
    @param connection: SQLAlchemy connect (with engine.connect() as connection:)
    @param table: 삭제할 테이블 metadata (not table name)
    @raises Exception: 함수 호출 시, Exception을 처리해야 한다.
    """

    connection.execute(delete(table))
    connection.commit()


@exception_handler
def get_table_metadata(engine, table_name):
    """
    MySQL Database에서 table_name과 일치하는 테이블을 찾고,
    해당 테이블에 해당하는 metadata를 반환하는 함수.
    table metadata = table을 구성하는 정보가 담긴 데이터를 table metadata라고 함
    :param engine: SQLAlchemy 엔진 객체
    :param table_name: 테이블 이름
    :return table: 테이블 metadata를 반환한다
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]
    return table


@exception_handler
def get_all_tables_from_database(engine):
    """
    MySQL 데이터베이스의 DatabaseInfo.database_name 스키마에 존재하는
    모든 테이블 메타데이터에서 table name string을 가져와주는 함수
    :return: table name list
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    all_tables = list(metadata.tables)
    return all_tables


@exception_handler
def insert_into_all_tables(engine, dummy_data, mode):
    """
    dummy_data에 모든 테이블에 넣을 데이터 dictionary를 전달받아서,
    sqlalchemy 함수를 이용해서 dictionary value들을 자동으로 넣어버리는 작업
    """
    with engine.connect() as connection:
        for table_name in dummy_data.keys():
            table_metadata = get_table_metadata(engine, table_name)
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table_metadata)
            connection.execute(table_metadata.insert(), dummy_data[table_name])
            connection.commit()


@exception_handler
def insert_dummy_data(engine, table_name, dummy_data, mode):
    """
    하나씩 구체적으로 생성된 더미데이터를 원하는 테이블에 삽입해주는 함수
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


# 해당 COL의 모든 CONSTRAINT및 잡다한 정보를 가져와주는 함수
@exception_handler
def get_column_type_detail(table, column):
    """
    `table`의 특정한 `column`에 대해 상세한 데이터 타입 정보를 가져오는 함수.
    type, size, decimal, enum, primary, unique 정보를 획득하여 dictonray에 저장한다.
    :param table:
    :param column:
    :return: column의 상세 정보가 담긴 dictionary를 반환한다. dictionary key는 'table_name', 'col_name', 'type', 'size',
             'decimal_place', 'enum_values', 'primary', 'unique'이다.
             - 'type'은 데이터 타입 (예: VARCHAR, INT 등)
             - 'size'는 데이터 타입의 크기 (예: VARCHAR(255)에서 255)
             - 'decimal_place'는 소수점 이하 자릿수 (NUMERIC 타입에서 사용)
             - 'enum_values'는 ENUM 타입의 경우 가능한 값들의 리스트
             - 'primary'는 해당 컬럼이 기본 키(primary key)일 경우 'True'
             - 'unique'는 해당 컬럼이 유니크(unique constraint)일 경우 'True'
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


def create_all_dummy_helper(fake, table, n):
    dummy_data = []
    for i in range(n):
        # n개의 더미 데이터 생성
        check_duplicate = set()
        data_row = {}
        for column in table.columns:
            if str(column.autoincrement) == "True":
                continue
            type_detail = get_column_type_detail(table, column)  # 해당 column의 상세정보를 dictionary 형태로 가져와줌
            data_row[column.name] = generate_data_at_once(fake, type_detail, check_duplicate)  # Row 하나씩 더미데이터 생성해줌
        dummy_data.append(data_row)  # 리스트에 저장

    return dummy_data


def create_all_dummy(engine, fake, n, mode):
    """
    모든 테이블의 메타데이터를 get_all_tables_from_database()를 통해 가져온 뒤,
    dictionary에 모든 더미데이터를 저장해서 insert_into_all_tables()에 넘겨주는 작업을 수행하는 함수
    """
    table_list = get_all_tables_from_database(engine)
    all_dummy_data = {}
    for table in table_list:
        # 테이블 메타데이터마다 더미데이터 n개 생성
        table_metadata = get_table_metadata(engine, table)
        generated_data = create_all_dummy_helper(fake, table_metadata, n)  # 데이터 리스트를 받아서
        all_dummy_data[table_metadata.name] = generated_data  # 테이블이름을 key로 가지는 dictionary에 행마다 넣을 데이터 리스트들 value로 저장

    insert_into_all_tables(engine, all_dummy_data, mode)  # 싹다 삽입


@exception_handler
def is_column_primary_key(engine, table_name, col_name):
    meta_table = get_table_metadata(engine, table_name)
    for column in meta_table.columns:
        if col_name == str(column.name):
            return column.primary_key
    return False


@exception_handler
def make_column_details_dictionary(engine, inspector, table_name, db_info):
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
def get_ddl_script(engine):
    # https://stackoverflow.com/questions/64677402/get-ddl-from-existing-databases-sqlalchemy
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_name = input('테이블 명 입력 : ')
    if table_name in table_mapper().keys():
        for table in metadata.sorted_tables:
            if table.name == table_name:
                print(CreateTable(table).compile(engine))
                break


@exception_handler
def get_view_list_details(engine, inspector: Inspector, db_info: DatabaseInfo):
    result = {}
    for view_name in inspector.get_view_names(db_info.database_name):
        view_definition = inspector.get_view_definition(view_name)

        # view columns
        re_aliases = re.findall(r'AS\s+`(\w+)`', view_definition)

        # real table name
        re_table_name = re.findall(r'FROM\s+`(\w+)`', view_definition, re.IGNORECASE)

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
