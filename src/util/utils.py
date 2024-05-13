import platform
import os


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
