"""
Manages database connection to read from it and write to it.
Author: {^^}
Date: 2025-11-04
"""


import json
from pathlib import Path
from typing import Any, Self, Dict

from recall.errors import (
    DatabaseWriteError, 
    DatabaseReadError, 
    DatabaseReadJsonError, 
    DatabaseNotFoundError
)


class JsonDatabaseManager:
    """Manager read and write to json db_file."""

    def __init__(self, db_file: Path) -> None:
        self._db_file = db_file

    def dump(self, data: Any) -> None:
        try:
            with open(self._db_file, "w") as file:
                json.dump(data, file, indent=4)
        except IOError:
            raise DatabaseWriteError(f"unable to write to database: '{self._db_file}'")

    def load(self) -> Dict[str, Any]:
        try:
            with open(self._db_file, "r") as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError:
            raise DatabaseReadJsonError(f"invalid json found in database: '{self._db_file}'")
        except Exception:
            raise DatabaseReadError(f"unable to read from database: '{self._db_file}'")

    @staticmethod
    def init_db(db_file: Path) -> None:
        try:
            with open(db_file, "w") as file:
                json.dump({}, file)
        except OSError as e:
            raise DatabaseWriteError(f"Error: writing to database {db_file}") from e

    @classmethod
    def factory(cls, db_file: Path) -> Self:
        if not db_file.exists():
            raise DatabaseNotFoundError(f"database not found at {db_file}")
        return cls(db_file)