import re

from sqlalchemy import MetaData, delete, text

from util.dummy_generators import generate_data_at_once
from util.error.error_handler import exception_handler


@exception_handler
def execute_sql_file(engine, file_path):
    """
    데이터베이스가 존재하지 않은 경우, engine connection을 이용해서
    DDL을 읽고, 해당 내용을 DB에 적용하는 함수.
    DDL 파일을 보면, 'NOT EXIST'라는 문구가 존재하기 때문에
    여러번 실행해도 기존 내용을 덮어쓰지 않는다
    :param engine: 데이터베이스에 연결할 엔진
    :param file_path: DDL 위치
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as file:  # file_path에서 read only, 선택한 encoding으로 파일 열기
        sql_commands = file.read()  # 파일 전체를 읽어서, sql_commands 객체가 built-in function인 open이 읽은 내용을 가리키게됨
    with engine.connect() as connection:
        for command in sql_commands.split(';'):  # SQL Query는 모두 ';'단위로 실행하므로 ';'로 split해서 리스트에 저장
            command = command.strip()  # command 양옆에 존재하는 공백 싹다 삭제해야 정상적으로 작동
            if command:
                connection.execute(text(command))  # string type command를 text로 변환해서 쿼리 실행


@exception_handler
def print_table(engine, table_name):
    """
    SQLAlchemy 엔진 객체와 테이블 이름을 사용하여 SQL 쿼리를 실행하고,
    결과를 콘솔에 출력해준다. 함수는 데이터베이스 연결을 관리하며, SELECT 쿼리를 통해
    테이블의 모든 데이터를 검색한다.

    :param engine: SQLAlchemy 엔진 객체
    :param table_name: 조회할 데이터베이스 테이블의 이름입니다.
    :raises Exception: 함수 호출 시, Exception을 처리해야 한다.
    """
    with engine.connect() as connection:
        sql = text("SELECT * FROM " + table_name)
        result = connection.execute(sql)
        conv_result = result.mappings().all()
        print(f'\n<<<<<<<<<<<<<<<<<<<<<<<<<<< {table_name} 더미데이터 내역 >>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        for dic in conv_result:
            print(dic)


@exception_handler
def delete_current_data(connection, table):
    """
    SQLAlchemy를 통해 table을 삭제해주는 함수.
    :param connection: SQLAlchemy connect (with engine.connect() as connection:)
    :param table: 삭제할 테이블 metadata (not table name)
    :return
    :raises Exception: 함수 호출 시, Exception을 처리해야 한다.
    """

    connection.execute(delete(table))
    connection.commit()


@exception_handler
def get_table_metadata(engine, table_name):
    """
    MySQL Database에서 table_name과 일치하는 테이블을 찾고,
    해당 테이블에 해당하는 metadata를 반환하는 함수.
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
    metadata = MetaData()
    metadata.reflect(bind=engine)
    all_tables = list(metadata.tables.keys())
    return all_tables


@exception_handler
def insert_into_all_tables(engine, dummy_data, mode):
    with engine.connect() as connection:
        for table_name in dummy_data.keys():
            meta_table = get_table_metadata(engine, table_name)
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, meta_table)
            connection.execute(meta_table.insert(), dummy_data[table_name])
            connection.commit()


@exception_handler
def insert_dummy_data(engine, table_name, dummy_data, mode):
    # DB에서 테이블 원형 가져오기
    table = get_table_metadata(engine, table_name)

    with engine.connect() as connection:
        if table_name == 'airline':
            # INSERT전, 모든 테이블 데이터 삭제
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "iata": data[0],
                    "airlinename": data[1],
                    "base_airport": data[2]})
        elif table_name == 'airport':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "iata": data[0],
                    "icao": data[1],
                    "name": data[2]
                })
        elif table_name == 'airplane_type':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "identifier": data[0],
                    "description": data[1]
                })
        elif table_name == 'airplane':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "capacity": data[0],
                    "type_id": data[1],
                    "airline_id": data[2]
                })
        elif table_name == 'airport_geo':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "airport_id": data[0],
                    "name": data[1],
                    "city": data[2],
                    "country": data[3],
                    "latitude": data[4],
                    "longitude": data[5],
                })
        elif table_name == 'airport_reachable':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "airport_id": data[0],
                    "hops": data[1]
                })
        elif table_name == 'booking':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "flight_id": data[0],
                    "seat": data[1],
                    "passenger_id": data[2],
                    "price": data[3],
                })
        elif table_name == 'employee':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "firstname": data[0],
                    "lastname": data[1],
                    "birthdate": data[2],
                    "sex": data[3],
                    "street": data[4],
                    "city": data[5],
                    "zip": data[6],
                    "country": data[7],
                    "emailaddress": data[8],
                    "telephoneno": data[9],
                    "salary": data[10],
                    "department": data[11],
                    "username": data[12],
                    "password": data[13]
                })
        elif table_name == 'flight_log':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "log_date": data[0],
                    "user": data[1],
                    "flight_id": data[2],
                    "flightno_old": data[3],
                    "flightno_new": data[4],
                    "from_old": data[5],
                    "to_old": data[6],
                    "from_new": data[7],
                    "to_new": data[8],
                    "departure_old": data[9],
                    "arrival_old": data[10],
                    "departure_new": data[11],
                    "arrival_new": data[12],
                    "airplane_id_old": data[13],
                    "airplane_id_new": data[14],
                    "airline_id_old": data[15],
                    "airline_id_new": data[16],
                    "comment": data[17]
                })
        elif table_name == 'flightschedule':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "flightno": data[0],
                    "from": data[1],
                    "to": data[2],
                    "departure": data[3],
                    "arrival": data[4],
                    "airline_id": data[5],
                    "monday": data[6],
                    "tuesday": data[7],
                    "wednesday": data[8],
                    "thursday": data[9],
                    "friday": data[10],
                    "saturday": data[11],
                    "sunday": data[12]
                })
        elif table_name == 'flight':
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "flightno": data[0],
                    "from": data[1],
                    "to": data[2],
                    "departure": data[3],
                    "arrival": data[4],
                    "airline_id": data[5],
                    "airplane_id": data[6]
                })
        elif table_name == "passenger":
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "passportno": data[0],
                    "firstname": data[1],
                    "lastname": data[2]
                })
        elif table_name == "passengerdetails":
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "passenger_id": data[0],
                    "birthdate": data[1],
                    "sex": data[2],
                    "street": data[3],
                    "city": data[4],
                    "zip": data[5],
                    "country": data[6],
                    "emailaddress": data[7],
                    "telephoneno": data[8]
                })
        elif table_name == "weatherdata":
            if mode == 'y' or mode == 'Y':
                delete_current_data(connection, table)
            for data in dummy_data:
                connection.execute(table.insert(), {
                    "log_date": data[0],
                    "time": data[1],
                    "station": data[2],
                    "temp": data[3],
                    "humidity": data[4],
                    "airpressure": data[5],
                    "wind": data[6],
                    "weather": data[7],
                    "winddirection": data[8]
                })
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
            type_detail = get_column_type_detail(table, column)
            data_row[column.name] = generate_data_at_once(fake, type_detail, check_duplicate)
        dummy_data.append(data_row)

    return dummy_data


def create_all_dummy(engine, fake, n, mode):
    table_list = get_all_tables_from_database(engine)
    all_dummy_data = {}
    for table in table_list:
        meta_table = get_table_metadata(engine, table)
        generated_data = create_all_dummy_helper(fake, meta_table, n)
        all_dummy_data[meta_table.name] = generated_data

    insert_into_all_tables(engine, all_dummy_data, mode)


def is_column_primary_key(engine, table_name: str, col_name: str):
    meta_table = get_table_metadata(engine, table_name)
    for column in meta_table.columns:
        if col_name == str(column.name):
            return column.primary_key
