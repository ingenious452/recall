from pathlib import Path

from .database import JsonDatabaseManager


# assuming all check to validate the path has been performed
# and user simply want to initialize database at this point
def init_db(db_file: Path) -> None:
    return JsonDatabaseManager.init_db(db_file)


def get_db(db_file: Path) -> JsonDatabaseManager:
    return JsonDatabaseManager.factory(db_file)


# this helps provide an interface to the database package
__all__ = ["init_db", "get_db", "JsonDatabaseManager"]