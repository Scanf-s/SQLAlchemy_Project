import os
import platform
from typing import Union, Tuple, Dict, Callable, Any

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


def clean_console() -> None:
    """
    Clears the console based on the operating system.

    @return: None
    """
    if platform.system() == "Windows":
        os.system('cls')  # 윈도우 CMD
    else:
        os.system('clear')  # 윈도우 Powershell, Linux, macOS


def print_menu() -> None:
    """
    Prints the main menu for the dummy data generation program.

    @return: None
    """
    print("\n더미 데이터 생성 프로그램")
    print("\n1. Generate Dummy one by one")
    print("\n2. Generate Dummy all in one")
    print("\n3. MySQL Management")
    print("\n4. Check generated dummy")
    print("\n5. Quit program")


def user_input(choice: str) -> Union[Tuple[int, str, str], Tuple[int, str], None]:
    """
    Processes user input and returns the corresponding values based on the choice.

    @param choice: User's choice as a string ('1' or '2')
    @return: A tuple containing the number of records and mode, and optionally the table name.
             - If choice == '1', returns (num_records, mode, table_name)
             - If choice == '2', returns (num_records, mode)
    @raise ValueError: If the mode is not 'y', 'Y', 'n', or 'N'
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


def table_mapper() -> Dict[str, Callable]:
    """
    Returns a dictionary mapping table names to their corresponding data generation functions.

    This function can be used like a dictionary:
    table_mapper()[key] = 'value'

    @return: Dictionary where keys are table names in the database schema (like airportdb)
    and values are the corresponding data generation function names.
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
