import sys

from faker import Faker
from sqlalchemy import Engine
from sqlalchemy import Inspector

from config.DatabaseInfo import DatabaseInfo
from util.database_utils import (
    insert_dummy_data,
    create_all_dummy,
    print_table,
    make_column_details_dictionary,
    get_ddl_script,
    get_view_list_details,
    create_mysql_view,
    get_column_names, get_table_metadata
)
from util.error.error_handler import exception_handler
from util.utils import clean_console, print_menu, table_mapper, user_input


@exception_handler
def main_user_interface(engine: Engine, fake: Faker, inspector: Inspector, db_info: DatabaseInfo) -> None:
    """
    Main user interface for the dummy data generation and database management program.

    @param engine: SQLAlchemy engine object connected to the target database
    @param fake: Faker object used to generate fake data
    @param inspector: SQLAlchemy Inspector object for reflecting database metadata
    @param db_info: DatabaseInfo object containing the database connection information
    @return: None
    """

    while True:
        clean_console()
        print_menu()
        choice = input("메뉴 입력: ")

        # Create dummy data by table name
        if choice == '1':
            clean_console()
            num_records, mode, table_name = user_input(choice)
            if table_name in table_mapper().keys():
                dummy_data = table_mapper()[table_name](fake, num_records)
                insert_dummy_data(engine, table_name, dummy_data, mode)
                print("데이터를 정상적으로 적용했습니다.")
            else:
                print("올바른 테이블명을 입력해주세요.")

        # Create dummy at once
        elif choice == '2':
            clean_console()
            num_records, mode = user_input(choice)
            create_all_dummy(engine, fake, num_records, mode)

        # Using Sqlalchemy inspector
        elif choice == '3':
            clean_console()
            schema_inspector_user_interface(engine, inspector, db_info)

        # Print dummy data
        elif choice == '4':
            clean_console()
            table_name = input("테이블 이름을 정확히 입력해주세요: ")
            # 존재하지 않는 테이블을 가져왔다면
            if table_name not in table_mapper().keys():
                print("테이블 이름이 정확하지 않습니다")
            else:
                print_table(engine, table_name)

        # 프로그램 종료
        elif choice == '5':
            clean_console()
            sys.exit(0)

        else:
            print("다시 입력해 주세요.")

        input("엔터를 누르면 초기화면으로 되돌아갑니다...")


def schema_inspector_user_interface(engine: Engine, inspector: Inspector, db_info: DatabaseInfo) -> None:
    """
    Provides a user interface for database schema inspection and management.

    @param engine: SQLAlchemy engine object connected to the target database
    @param inspector: SQLAlchemy Inspector object for reflecting database metadata
    @param db_info: DatabaseInfo object containing the database connection information
    @return: None
    """

    print("Database Management Menu")
    print("1. 현재 접속한 Database정보 및 schema 목록")
    print("2. 현재 선택한 Schema에 속한 테이블 목록")
    print("3. 현재 선택한 Schema에 속한 뷰 목록")
    print("4. 현재 선택한 Schema에 속한 테이블 목록, 테이블 별 Column 정보, 코멘트 목록 조회")
    print("5. 현재 선택한 Schema에 속한 뷰 목록과 뷰 별 Column 정보, 코멘트 목록 조회")
    print("6. 특정 테이블의 Column 명 출력")
    print("7. 특정 테이블의 Column 정보, Comment 조회")
    print("8. 특정 테이블의 DDL 스크립트 생성")
    print("9. 새로운 View 생성")
    print("10. 메인으로 돌아가기")
    menu = int(input("메뉴 입력 : "))

    if menu == 1:
        print(f"접속 정보 : {engine.url}")
        print(f"해당 접속에 대한 Schema 리스트 : {inspector.get_schema_names()}")

    elif menu == 2:
        print(f"현재 선택된 Schema : {db_info.database_name}")
        print(f"{db_info.database_name}에 속한 테이블 리스트 : {inspector.get_table_names(db_info.database_name)}")

    elif menu == 3:
        print(f"뷰 리스트 : {inspector.get_view_names(db_info.database_name)}")

    elif menu == 4:
        result = []
        tables = inspector.get_table_names(db_info.database_name)
        for table in tables:
            result.append(make_column_details_dictionary(engine, inspector, table, db_info))
        for i in result:
            print(i)

    elif menu == 5:
        result = get_view_list_details(engine, inspector, db_info)
        for key, value in result.items():
            print(key, value)

    elif menu == 6:
        result = []
        table_name = input("테이블 명 입력 : ")
        if table_name in table_mapper().keys():
            result.append(get_column_names(engine, inspector, table_name, db_info))
            print(result)
        else:
            print("올바른 테이블명을 입력해주세요.")

    elif menu == 7:
        result = []
        table_name = input("테이블 명 입력 : ")
        if table_name in table_mapper().keys():
            result.append(make_column_details_dictionary(engine, inspector, table_name, db_info))
            print(result)
        else:
            print("올바른 테이블명을 입력해주세요.")

    elif menu == 8:
        get_ddl_script(engine)

    elif menu == 9:
        table_name = input("테이블 명을 입력하세요 : ")
        table_metadata = get_table_metadata(engine, table_name)
        create_mysql_view(engine, inspector, table_metadata, db_info)

    elif menu == 10:
        pass
