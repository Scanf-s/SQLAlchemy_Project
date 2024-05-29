from typing import Dict, Callable

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
