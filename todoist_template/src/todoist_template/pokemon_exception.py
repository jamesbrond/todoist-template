"""Pokemon Exceptions - Gonna catch 'em all!"""

import logging
import sys
import httpx
from todoist_template.i18n import _t


class PokemonException(Exception):
    """Custom exception class for Pokemon exceptions to avoid re-handling the same exception multiple times."""
    pass


def pokemon_exception_handler_function_decorator(func):
    def func_wrapper(*args, **kwargs):
        exc_text = None
        exc = None
        exc_info = None
        try:
            return func(*args, **kwargs)
        except PokemonException as ex:
            # Already handled exception, re-raise it and avoid double handling
            raise
        except httpx.HTTPError as ex:
            exc = ex
            exc_text = _t("Network Error: There was an exception that occurred while handling your request")
            exc_info = sys.exc_info()
        except Exception as ex:
            exc = ex
            exc_info = sys.exc_info()
        finally:
            if exc is not None:
                logging.debug(f"Pokemon Exception Handled in {func.__qualname__}({kwargs})")
                logging.error(exc_text if exc_text else str(exc), exc_info=exc_info if exc_info else True)
                raise PokemonException(exc_text) from exc
    return func_wrapper


def pokemon_exception_handler_class_decorator(cls):
    def exception_wrapper(method):
        def wrapper(*args, **kwargs):
            return pokemon_exception_handler_function_decorator(method)(*args, **kwargs)
        return wrapper

    ## Apply wrapper to all methods
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, exception_wrapper(method))

    return cls
