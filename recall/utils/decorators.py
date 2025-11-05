import logging
from functools import wraps
from typing import Callable
from recall.config import config
from recall.errors import RecallReadError, RecallWriteError, DatabaseReadError, DatabaseReadJsonError, DatabaseWriteError



def with_datbase_access(operation_name: str):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            logger = logging.getLogger(self.__class__.__name__)
            fh = logging.FileHandler(config.LOGS_DIR / "service.log" )
            logger.addHandler(fh)

            try:
                return func(self, *args, **kwargs)
            except (DatabaseReadJsonError, DatabaseReadError) as e:
                logger.error(f"error: unable to '{operation_name}' to index, {e}")
                raise RecallReadError(f"cannot read or invalid json in database.") from e
            except DatabaseWriteError as e:
                logger.error(f"error unable to '{operation_name}' to database, {e}")
                raise RecallWriteError(f"cannot to write to database") from e
        return wrapper
    return decorator