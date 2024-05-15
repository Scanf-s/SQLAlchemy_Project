import functools
from sqlalchemy.exc import IntegrityError


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as ite:
            print(f"SQLAlchemy Integrity Error occured: {ite}")
        except KeyboardInterrupt as ki:
            print(f"User interrupt : {ki}")
        except ValueError as ve:
            print(f"ValueError occurred: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")

    return wrapper
