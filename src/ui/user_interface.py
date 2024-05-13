import sys

from src.util.utils import clean_console, print_menu
from src.util.dummy_generators import (
    generate_airline_data,
    generate_airport_data,
    generate_flight_data,
    generate_booking_data,
    generate_airplane_data,
    generate_employee_data,
    generate_passenger_data,
    generate_weatherdata_data,
    generate_flightschedule_data,
    generate_passengerdetails_data,
    generate_airport_geo_data,
    generate_flight_log_data,
    generate_airplane_type_data,
    generate_airport_reachable_data
)
from src.util.database_utils import (
    get_all_tables_from_database,
    insert_dummy_data,
    create_all_dummy,
    print_table
)


def run(engine, fake):
    while True:
        try:
            clean_console()
            print_menu()
            choice = input("메뉴 입력: ")

            # 더미 데이터 생성
            if choice == '1':
                clean_console()
                table_lists = get_all_tables_from_database(engine)

                num_records = int(input("얼마나 생성할까요?: "))
                mode = input("테이블을 초기화하고 새로 입력하시겠습니까? [y/n]: ")
                if not (mode == 'y' or mode == 'Y' or mode == 'n' or mode == 'N'):
                    raise ValueError("유효하지 않은 모드 선택: 모드는 'y/Y' 또는 'n/N' 이어야 합니다.")
                table_name = input("테이블 이름을 정확히 입력해주세요: ")

                # 존재하지 않는 테이블을 가져왔다면
                if table_name not in table_lists:
                    raise ValueError(f"테이블 이름 '{table_name}'은(는) 유효하지 않습니다. 가능한 테이블 이름을 확인해주세요.")
                try:
                    if table_name == 'airline':
                        dummy_data = generate_airline_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'airport':
                        dummy_data = generate_airport_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'airplane_type':
                        dummy_data = generate_airplane_type_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'airplane':
                        dummy_data = generate_airplane_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'airport_geo':
                        dummy_data = generate_airport_geo_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'airport_reachable':
                        dummy_data = generate_airport_reachable_data(fake,num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'booking':
                        dummy_data = generate_booking_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'employee':
                        dummy_data = generate_employee_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'flight_log':
                        dummy_data = generate_flight_log_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'flightschedule':
                        dummy_data = generate_flightschedule_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'flight':
                        dummy_data = generate_flight_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'passenger':
                        dummy_data = generate_passenger_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'passengerdetails':
                        dummy_data = generate_passengerdetails_data(fake,num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    elif table_name == 'weatherdata':
                        dummy_data = generate_weatherdata_data(fake, num_records)
                        insert_dummy_data(engine, table_name, dummy_data, mode)
                        print("데이터를 정상적으로 적용했습니다.")
                    else:
                        print("올바른 테이블명을 입력해주세요.")
                except ValueError as ve:
                    print(f"입력 오류: {ve}")
                except Exception as e:
                    print("Exception Occurs : ", e)

            elif choice == '2':
                clean_console()
                num_records = int(input("얼마나 생성할까요?: "))
                mode = input("테이블을 초기화하고 새로 입력하시겠습니까? [y/n]: ")
                if not (mode == 'y' or mode == 'Y' or mode == 'n' or mode == 'N'):
                    raise ValueError("유효하지 않은 모드 선택: 모드는 'y/Y' 또는 'n/N' 이어야 합니다.")
                create_all_dummy(engine, fake, num_records, mode)

            elif choice == '3':
                pass

            # 테스트 데이터 출력
            elif choice == '4':
                clean_console()
                table_lists = get_all_tables_from_database(engine)
                table_name = input("테이블 이름을 정확히 입력해주세요: ")
                # 존재하지 않는 테이블을 가져왔다면
                if table_name not in table_lists:
                    print("테이블 이름이 정확하지 않습니다")
                else:
                    print_table(engine, table_name)

            elif choice == '5':
                clean_console()
                sys.exit(0)
            else:
                print("다시 입력해 주세요.")
        except KeyboardInterrupt as ki:
            print(f"사용자 임의 종료 : {ki}")
            sys.exit(0)
        except Exception as e:
            print(f"Exceptions : {e}")