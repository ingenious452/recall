"""
Core recall logic that orchestrate everything.

Author: {^^}
Date: 2025-11-04
"""

import logging
from pathlib import Path
from typing import Any, Dict, Self, Optional

from recall.config import config

from recall.data import get_db, JsonDatabaseManager, init_db
from recall.utils.decorators import with_datbase_access

from recall.errors import (
    DatabaseNotFoundError,
    RecallInitError,
    RecallNotFoundError,
    RecallExistsError,

)


# we should use decorator pattern causes I am going to load and dump to database in each of th e call
class RecallOrchestrator:
    def __init__(self, db_handler: JsonDatabaseManager):
        self._db_handler = db_handler
        self._logger = logging.getLogger(__name__)

    @with_datbase_access("get")
    def get(self, recall_id_or_name: str | int) -> str:
        data = self._db_handler.load()
        if isinstance(recall_id_or_name, str):
            if entry := data.get(recall_id_or_name):
                return entry
        elif isinstance(recall_id_or_name, int):
            entries = [(key, value) for key, value in data.items()]
            if 1 <= recall_id_or_name <= len(entries):
                return entries[recall_id_or_name-1][1]
        raise RecallNotFoundError(f"entry [cyan]{recall_id_or_name}[/cyan] not found in database.")

    @with_datbase_access("add")
    def add(self, recall_name: str, recall_path: str) -> None:
        # Get the data from the database
        data = self._db_handler.load()
        # assuming users has provided a recall_name and
        # reall_path that are correct. and cli interface has validated everything already
        # I am putting whatever user has provided directly to the database without validating if it's already present in the database.
        # check if the data exists
        if recall_name in data:
            raise RecallExistsError(f"entry for [cyan]'{recall_name}'[/cyan] found in database.")
        data[recall_name] = recall_path  # should I do processing of text such as all lower case and such.
        self._db_handler.dump(data)
        return None

    @with_datbase_access("remove")
    def remove(self, recall_name: str) -> str:
        data = self._db_handler.load()
        if not (entry := data.pop(recall_name, None)):  # will not raise key error as a default value is provided
            raise RecallNotFoundError(f"entry for [cyan]'{recall_name}'[/cyan] not found in database.")
        self._db_handler.dump(data)
        return entry

    @with_datbase_access("update")
    def update(self, recall_name: str, recall_path: str) -> str:
        data = self._db_handler.load()
        if not (entry := data.get(recall_name)):
            raise RecallNotFoundError(f"entry for [cyan]'{recall_name}'[/cyan] not found in database.")
        data[recall_name] = recall_path
        self._db_handler.dump(data)
        return entry
    
    @with_datbase_access("show")
    def show(self) -> Dict[str, Any]:
        data = self._db_handler.load()
        return data

    @staticmethod
    def init_recall(db_file: Optional[Path], logs_dir: Optional[Path]):
        config.init_config(db_file, logs_dir)
        init_db(config.DATABASE_FILE)

    @classmethod
    def factory(cls) -> Self:
        # Check if user has executed init and created database file needed.
        # verify that the file exists and ready to be read
        if config.INITIALIZED:
            db_file = config.DATABASE_FILE
            try:
                db_handler = get_db(db_file)
            except DatabaseNotFoundError as e:
                raise RecallInitError("database not initialized") from e
            else:
                return cls(db_handler)
        raise RecallInitError("configuration not initialized")
