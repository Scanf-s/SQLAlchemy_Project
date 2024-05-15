import platform
import os

from util.dummy_generators import (
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


# 콘솔 지우는 함수
def clean_console():
    """
    운영체제에 따라 콘솔을 clear하도록 명령하는 함수
    :return: none
    """
    if platform.system() == "Windows":
        os.system('cls')  # for Windows
    else:
        os.system('clear')  # for Linux and macOS


def print_menu():
    print("\n더미 데이터 생성 프로그램")
    print("\n1. Generate Dummy one by one")
    print("\n2. Generate Dummy all in one")
    print("\n3. MySQL Management")
    print("\n4. Check generated dummy")
    print("\n5. Quit program")


def user_input(choice):

    """
    사용자 input을 처리하여 반환하는 함수
    :return num_records, mode, table_name: choice == 1인경우, 생성할 레코드 개수, 삭제 모드, 테이블 이름 순으로 반환합니다
    :return num_records, mode: choice == 2인경우
    """

    if choice == '1':
        num_records = int(input("얼마나 생성할까요?: "))
        mode = input("테이블을 초기화하고 새로 입력하시겠습니까? [y/n]: ")
        if not (mode == 'y' or mode == 'Y' or mode == 'n' or mode == 'N'):
            raise ValueError("유효하지 않은 모드 선택: 모드는 'y/Y' 또는 'n/N' 이어야 합니다.")
        table_name = input("테이블 이름을 정확히 입력해주세요: ")
        return num_records, mode, table_name

    elif choice == '2':
        num_records = int(input("얼마나 생성할까요?: "))
        mode = input("테이블을 초기화하고 새로 입력하시겠습니까? [y/n]: ")
        if not (mode == 'y' or mode == 'Y' or mode == 'n' or mode == 'N'):
            raise ValueError("유효하지 않은 모드 선택: 모드는 'y/Y' 또는 'n/N' 이어야 합니다.")
        return num_records, mode


def table_mapper():

    """
    이 함수를 함수 명이 저장된 dictionary처럼 사용할 수 있습니다.
    table_mapper()[key] = 'value' 형식을 통해 사용할 수 있습니다.
    :return dictionary: airportdb의 테이블명과 그 테이블에 맞는 데이터를 생성하는 함수명이 매핑되어 있습니다.
    """

    return {
        'airline': generate_airline_data,
        'airport': generate_airport_data,
        'airplane_type': generate_airplane_type_data,
        'airplane': generate_airplane_data,
        'airport_geo': generate_airport_geo_data,
        'airport_reachable': generate_airport_reachable_data,
        'booking': generate_booking_data,
        'employee': generate_employee_data,
        'flight_log': generate_flight_log_data,
        'flightschedule': generate_flightschedule_data,
        'flight': generate_flight_data,
        'passenger': generate_passenger_data,
        'passengerdetails': generate_passengerdetails_data,
        'weatherdata': generate_weatherdata_data
    }
