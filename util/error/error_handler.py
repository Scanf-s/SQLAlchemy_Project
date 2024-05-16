import functools
import traceback

from sqlalchemy.exc import IntegrityError


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IntegrityError as ite:
            print(traceback.format_exc())
        except KeyboardInterrupt as ki:
            print(traceback.format_exc())
        except ValueError as ve:
            print(traceback.format_exc())
        except Exception as e:
            print(traceback.format_exc())

    return wrapper
