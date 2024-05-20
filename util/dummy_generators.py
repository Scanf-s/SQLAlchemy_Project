import random
import string
from typing import Dict, Any, Set
from faker import Faker

from util.error.error_handler import exception_handler


def generate_airline_data(fake, n):
    """
    airportdb의 `airline` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """
    charset = string.ascii_letters + string.digits + string.punctuation
    check_duplicate_iata = set()
    dummy_data = []
    for i in range(n):
        airline_iata = fake.lexify(text='??', letters=charset)
        while airline_iata in check_duplicate_iata:
            airline_iata = fake.lexify(text='??', letters=charset)
        check_duplicate_iata.add(airline_iata)
        airline_name = fake.airline()
        base_airport = fake.random_int(min=0, max=32000)

    #    dummy_data.append((airline_iata, airline_name, base_airport))
        dummy_data.append(
            {
                "iata": airline_iata,
                "airlinename": airline_name,
                "base_airport": base_airport
            }
        )
    return dummy_data


def generate_airplane_data(fake, n):
    """
    airportdb의 `airplane` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    dummy_data = []
    for i in range(n):
        # mediumint unsigned : 0 ~ 16777215
        capacity = fake.random_int(min=2, max=10000000)
        type_id = fake.random_int(min=1, max=20001)
        airline_id = fake.random_int(min=1, max=32767)

        dummy_data.append(
            {
                "iata": capacity,
                "icao": type_id,
                "name": airline_id
            }
        )

    return dummy_data


def generate_airplane_type_data(fake, n):
    """
    airportdb의 `airplane_type` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    dummy_data = []
    for i in range(n):
        identifier = fake.bothify('??##', letters=string.ascii_uppercase)
        description = fake.text(max_nb_chars=100)

        dummy_data.append(
            {
                "identifier": identifier,
                "description": description
            }
        )

    return dummy_data


def generate_airport_data(fake, n):
    """
    airportdb의 `airport` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    check_duplicate_icao = set()
    dummy_data = []
    for i in range(n):
        airport_iata = fake.airport_iata()
        airport_icao = fake.airport_icao()
        while airport_icao in check_duplicate_icao:
            airport_icao = fake.airport_icao()
        check_duplicate_icao.add(airport_icao)
        airport_name = fake.airport_name()

        dummy_data.append(
            {
                "iata": airport_iata,
                "icao": airport_icao,
                "name": airport_name
            }
        )

    return dummy_data


def generate_airport_geo_data(fake, n):
    """
    airportdb의 `airport_geo` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    check_duplicate_airport_id = set()
    dummy_data = []
    for i in range(n):
        airport_id = fake.random_int(1, 32767)
        while airport_id in check_duplicate_airport_id:
            airport_id = fake.random_int(1, 32767)
        check_duplicate_airport_id.add(airport_id)
        name = fake.airport_name()
        city = fake.city()
        country = fake.country()
        latitude = fake.latitude()
        longitude = fake.longitude()

        dummy_data.append(
            {
                "airport_id": airport_id,
                "name": name,
                "city": city,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    return dummy_data


def generate_airport_reachable_data(fake, n):
    """
    airportdb의 `airport_reachable` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    check_duplicate_airport_id = set()
    dummy_data = []
    for i in range(n):
        airport_id = fake.random_int(1, 32767)
        while airport_id in check_duplicate_airport_id:
            airport_id = fake.random_int(1, 32767)
        check_duplicate_airport_id.add(airport_id)
        hops = fake.random_int(1, 100) if random.choice([True, False]) else None

        dummy_data.append(
            {
                "airport_id": airport_id,
                "hops": hops
            }
        )

    return dummy_data


def generate_booking_data(fake, n):
    """
    airportdb의 `booking` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    check_duplicate_flight_id = set()
    check_duplicate_seat = set()
    dummy_data = []

    for i in range(n):
        # 항공기 번호가 아니라, 예약 번호인 것 같다.
        flight_id = fake.random_int(100000, 500000)
        while flight_id in check_duplicate_flight_id:
            flight_id = fake.random_int(100000, 500000)
        check_duplicate_flight_id.add(flight_id)
        seat = fake.bothify('??##', letters=string.ascii_uppercase) if random.choice([True, False]) else None
        while seat in check_duplicate_seat:
            seat = fake.bothify('??##', letters=string.ascii_uppercase) if random.choice([True, False]) else None
        check_duplicate_seat.add(seat)
        passenger_id = fake.random_int(min=10000, max=30001)
        price = fake.pydecimal(right_digits=2, left_digits=8, positive=True, min_value=0.99, max_value=10000)

        dummy_data.append(
            {
                "flight_id": flight_id,
                "seat": seat,
                "passenger_id": passenger_id,
                "price": float(price),
            }
        )

    return dummy_data


def generate_employee_data(fake, n):
    """
    airportdb의 `employee` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    # from faker.generator import random
    check_duplicate_username = set()
    dummy_data = []
    for i in range(n):
        firstname = fake.first_name()
        lastname = fake.last_name()
        birthdate = fake.date_between()
        sex = fake.passport_gender() if random.choice([True, False]) else None
        street = fake.street_address()
        city = fake.city()

        zipcode = int(fake.zipcode())
        while not 0 <= zipcode <= 32767:
            zipcode = int(fake.zipcode())

        country = fake.country()
        emailaddress = fake.company_email() if random.choice([True, False]) else None
        telephoneno = fake.country_calling_code() + fake.basic_phone_number() if random.choice([True, False]) else None
        salary = fake.pydecimal(
            right_digits=2,
            left_digits=6,
            positive=True,
            min_value=2000,
            max_value=50000
        ) if random.choice([True, False]) else None

        # enum ('Marketing','Buchhaltung','Management','Logistik','Flugfeld']
        department_list = ['Marketing', 'Buchhaltung', 'Management', 'Logistik', 'Flugfeld']
        department = random.choice(department_list) if random.choice([True, False]) else None

        username = fake.user_name() if random.choice([True, False]) else None
        while username in check_duplicate_username:
            username = fake.user_name() if random.choice([True, False]) else None
        check_duplicate_username.add(username)

        password = fake.password(special_chars=True, length=32) if username is not None else None

        dummy_data.append(
            {
                "firstname": firstname,
                "lastname": lastname,
                "birthdate": birthdate,
                "sex": sex,
                "street": street,
                "city": city,
                "zip": zipcode,
                "country": country,
                "emailaddress": emailaddress,
                "telephoneno": telephoneno,
                "salary": salary,
                "department": department,
                "username": username,
                "password": password
            }
        )

    return dummy_data


def generate_flight_data(fake, n):
    """
    airportdb의 `flight` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """
    charset = string.ascii_letters + string.digits + string.punctuation
    check_duplicate_flightno = set()
    dummy_data = []
    for i in range(n):
        flightno = fake.bothify(text="???-####", letters=charset)
        while flightno in check_duplicate_flightno:
            flightno = fake.bothify(text="???-####", letters=charset)
        check_duplicate_flightno.add(flightno)

        _from = random.randint(1, 20001)
        _to = random.randint(1, 20001)
        departure_time = fake.date_time()
        arrival_time = fake.date_time_between(start_date=departure_time)
        airline_id = random.randint(1, 20001)
        airplane_id = random.randint(1, 20001)

        dummy_data.append(
            {
                "flightno": flightno,
                "from": _from,
                "to": _to,
                "departure": departure_time,
                "arrival": arrival_time,
                "airline_id": airline_id,
                "airplane_id": airplane_id
            }
        )

    return dummy_data


def generate_flight_log_data(fake, n):
    """
    airportdb의 `flight_log` 테이블에 들어가는 더미데이터를 생성하는 함수

    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """
    charset = string.ascii_letters + string.digits + string.punctuation
    dummy_data = []
    for i in range(n):
        log_date = fake.date_time_this_decade()
        user = fake.user_name()

        flight_id = random.randint(100000, 500000)

        flightno_old = fake.bothify(text='???-####', letters=charset)
        flightno_new = fake.bothify(text='???-####', letters=charset)

        from_old = random.randint(1, 100)
        to_old = random.randint(1, 100)
        from_new = random.randint(1, 100)
        to_new = random.randint(1, 100)

        departure_old = fake.date_time_this_year(before_now=True, after_now=False)
        arrival_old = fake.date_time_this_year(before_now=True, after_now=False)
        departure_new = fake.date_time_this_year(before_now=False, after_now=True)
        arrival_new = fake.date_time_this_year(before_now=False, after_now=True)

        airplane_id_old = random.randint(1, 20001)
        airplane_id_new = random.randint(1, 20001)
        airline_id_old = random.randint(1, 20001)
        airline_id_new = random.randint(1, 20001)

        comment = fake.text(max_nb_chars=200) if random.choice([True, False]) else None

        dummy_data.append(
            {
                "log_date": log_date,
                "user": user,
                "flight_id": flight_id,
                "flightno_old": flightno_old,
                "flightno_new": flightno_new,
                "from_old": from_old,
                "to_old": to_old,
                "from_new": from_new,
                "to_new": to_new,
                "departure_old": departure_old,
                "arrival_old": arrival_old,
                "departure_new": departure_new,
                "arrival_new": arrival_new,
                "airplane_id_old": airplane_id_old,
                "airplane_id_new": airplane_id_new,
                "airline_id_old": airline_id_old,
                "airline_id_new": airline_id_new,
                "comment": comment
            }
        )

    return dummy_data


def generate_flightschedule_data(fake, n):
    """
    airportdb의 `flight_schedule` 테이블에 들어가는 더미데이터를 생성하는 함수

    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    charset = string.ascii_letters + string.digits + string.punctuation
    check_duplicate_flightno = set()
    dummy_data = []
    for i in range(n):
        flightno = fake.bothify(text="???-####", letters=charset)
        while flightno in check_duplicate_flightno:
            flightno = fake.bothify(text="???-####", letters=charset)
        check_duplicate_flightno.add(flightno)

        _from = random.randint(1, 20001)
        _to = random.randint(1, 20001)

        departure_time = fake.time()
        arrival_time = fake.time()

        airline_id = random.randint(1, 20001)

        monday = 1 if random.choice([True, False]) else 0
        tuesday = 1 if random.choice([True, False]) else 0
        wednesday = 1 if random.choice([True, False]) else 0
        thursday = 1 if random.choice([True, False]) else 0
        friday = 1 if random.choice([True, False]) else 0
        saturday = 1 if random.choice([True, False]) else 0
        sunday = 1 if random.choice([True, False]) else 0

        dummy_data.append(
            {
                "flightno": flightno,
                "from": _from,
                "to": _to,
                "departure": departure_time,
                "arrival": arrival_time,
                "airline_id": airline_id,
                "monday": monday,
                "tuesday": tuesday,
                "wednesday": wednesday,
                "thursday": thursday,
                "friday": friday,
                "saturday": saturday,
                "sunday": sunday
            }
        )

    return dummy_data


def generate_passenger_data(fake, n):
    """
    airportdb의 `passenger` 테이블에 들어가는 더미데이터를 생성하는 함수

    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    check_duplicate_passportno = set()
    dummy_data = []
    for i in range(n):
        passportno = fake.passport_number()
        while passportno in check_duplicate_passportno:
            passportno = fake.passport_number()
        check_duplicate_passportno.add(passportno)

        first_name = fake.first_name()
        last_name = fake.last_name()

        dummy_data.append(
            {
                "passportno": passportno,
                "firstname": first_name,
                "lastname": last_name
            }
        )
    return dummy_data


def generate_passengerdetails_data(fake, n):
    """
    airportdb의 `passenger_details` 테이블에 들어가는 더미데이터를 생성하는 함수

    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    check_duplicate_passenger_id = set()
    dummy_data = []
    for i in range(n):
        passenger_id = random.randint(1, 20001)
        while passenger_id in check_duplicate_passenger_id:
            passenger_id = random.randint(1, 20001)
        check_duplicate_passenger_id.add(passenger_id)

        birthdate = fake.date()
        sex = fake.passport_gender() if random.choice([True, False]) else None
        street = fake.street_address()
        city = fake.city()
        zipcode = int(fake.zipcode())
        while not 0 <= zipcode <= 32767:
            zipcode = int(fake.zipcode())
        country = fake.country()
        emailaddress = fake.company_email() if random.choice([True, False]) else None
        telephoneno = fake.country_calling_code() + fake.basic_phone_number() if random.choice([True, False]) else None

        dummy_data.append(
            {
                "passenger_id": passenger_id,
                "birthdate": birthdate,
                "sex": sex,
                "street": street,
                "city": city,
                "zip": zipcode,
                "country": country,
                "emailaddress": emailaddress,
                "telephoneno": telephoneno
            }
        )

    return dummy_data


@exception_handler
def generate_weatherdata_data(fake, n):
    """
    airportdb의 `weatherdata` 테이블에 들어가는 더미데이터를 생성하는 함수
    :param fake: fake 라이브러리 사용을 위한 객체
    :param n: 더미데이터를 생성할 개수
    :return: 생성한 더미 데이터를 반환합니다.
    """

    check_duplicate_log_date = set()
    check_duplicate_time = set()
    check_duplicate_station = set()
    dummy_data = []
    for i in range(n):
        log_date = fake.date()
        while log_date in check_duplicate_log_date:
            log_date = fake.date()
        check_duplicate_log_date.add(log_date)

        _time = fake.time()
        while _time in check_duplicate_time:
            _time = fake.time()
        check_duplicate_time.add(_time)

        station = random.randint(1, 20001)
        while station in check_duplicate_station:
            station = random.randint(1, 20001)
        check_duplicate_station.add(station)

        temperature = float(fake.pydecimal(left_digits=2, right_digits=1, positive=True))
        humidity = float(fake.pydecimal(left_digits=3, right_digits=1, positive=True))
        airpressure = float(fake.pydecimal(left_digits=8, right_digits=2, positive=True))
        wind = float(fake.pydecimal(left_digits=3, right_digits=2, positive=True))
        weather_enums = ['Nebel-Schneefall', 'Schneefall', 'Regen', 'Regen-Schneefall', 'Nebel-Regen',
                         'Nebel-Regen-Gewitter', 'Gewitter', 'Nebel', 'Regen-Gewitter']
        weather = random.choice(weather_enums) if random.choice([True, False]) else None
        winddirection = random.randint(0, 360)

        dummy_data.append(
            {
                "log_date": log_date,
                "time": _time,
                "station": station,
                "temp": temperature,
                "humidity": humidity,
                "airpressure": airpressure,
                "wind": wind,
                "weather": weather,
                "winddirection": winddirection
            }
        )

    return dummy_data


def generate_distinct_integer(data_type: str, check_num_duplicate: Set[int]) -> int:
    """
    Function to generate distinct integer

    @param data_type:
    @param check_num_duplicate:
    @return: Returns generated unique integer
    """

    generated_int = random.randint(1, 20001) if data_type != "TINYINT" else random.randint(0, 2)
    while generated_int in check_num_duplicate:
        generated_int = random.randint(1, 20001) if data_type != "TINYINT" else random.randint(0, 2)
    check_num_duplicate.add(generated_int)
    return generated_int


def generate_distinct_characters(fake: Faker, charset: str, size: int, check_str_duplicate: Set[str]) -> str:
    """
    Function to generate distinct characters or string type

    @param fake:
    @param charset:
    @param size:
    @param check_str_duplicate:
    @return: Returns generated unique characters (String)
    """

    generated_char = fake.lexify('?' * size, letters=charset)
    while generated_char in check_str_duplicate:
        generated_char = fake.lexify('?' * size, letters=charset)
    check_str_duplicate.add(str(generated_char))
    return generated_char


@exception_handler
def generate_data_with_type(fake: Faker, type_detail: Dict[str, Any], check_str_duplicate: Set[str], check_num_duplicate: Set[int]) -> Any:
    """
    Generate data using type_detail

    @param fake:
    @param type_detail:
    @param check_str_duplicate:
    @param check_num_duplicate:
    @return: Returns one specific type of data
    """

    data_type = type_detail['type']
    size = type_detail['size']
    decimal_place = type_detail.get('decimal_place')
    is_primary = type_detail.get('primary') == 'True'
    is_unique = type_detail.get('unique') == 'True'

    if data_type in ["INTEGER", "SMALLINT", "MEDIUMINT", "TINYINT"]:
        if is_primary or is_unique:
            return generate_distinct_integer(data_type, check_num_duplicate)
        else:
            # TINYINT가 적용된 column이 0 또는 1만 사용하므로
            return random.randint(1, 20001) if data_type != "TINYINT" else random.randint(0, 2)

    elif data_type in ["CHAR", "VARCHAR", "TEXT"]:
        charset = string.ascii_letters + string.digits + string.punctuation
        if data_type == "CHAR" and size:  # char
            if is_primary or is_unique:
                return generate_distinct_characters(fake, charset, size, check_str_duplicate)
            return fake.lexify('?' * size, letters=charset)
        elif data_type == "VARCHAR" and size:  # varchar
            if is_primary or is_unique:
                return generate_distinct_characters(fake, charset, size, check_str_duplicate)
            return fake.text(max_nb_chars=size)
        else:  # text
            return fake.text()

    elif data_type in ["DECIMAL"]:
        if size and decimal_place:
            max_value = 10 ** (size - decimal_place) - 1
            return round(random.uniform(0, max_value), decimal_place)
        else:
            return round(random.uniform(0, 10000), 2)

    elif data_type in ["DATE"]:
        return fake.date()

    elif data_type in ["TIME"]:
        return fake.time()

    elif data_type in ["DATETIME"]:
        return fake.date_time()

    elif data_type in ["ENUM"]:
        if 'enum_values' in type_detail:
            return random.choice(type_detail['enum_values'])
        else:
            return None

    else:
        return None
