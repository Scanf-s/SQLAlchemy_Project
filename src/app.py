from faker import Faker
from faker_airtravel import AirTravelProvider

from src.ui.user_interface import run
from src.config.db import create_connection


if __name__ == "__main__":
    engine = create_connection()
    fake = Faker()
    fake.add_provider(AirTravelProvider)
    run(engine, fake)

