"""
Core recall logic that orchestrate everything.

Author: {^^}
Date: 2025-11-04
"""

import logging
from pathlib import Path
from typing import Any, Dict, Self, Tuple, Optional

from recall.config import config

from recall.data import get_db, JsonDatabaseManager, init_db

from recall.errors import (
    DatabaseNotFoundError,
    DatabaseReadJsonError,
    DatabaseReadError,
    DatabaseWriteError,
    RecallInitError,
    RecallNotFoundError,
    RecallReadError,
    RecallWriteError,
    RecallExistsError,

)


# we should use decorator pattern causes I am going to load and dump to database in each of th e call
class RecallOrchestrator:
    def __init__(self, db_handler: JsonDatabaseManager):
        self._db_handler = db_handler
        self._logger = logging.getLogger(__name__)

    def get(self, recall_id_or_name: str | int) -> str:
        self._logger.info(f"Retrieving {recall_id_or_name}.")
        try:
            data = self._db_handler.load()
            if isinstance(recall_id_or_name, str):
                if entry := data.get(recall_id_or_name):
                    return entry
            elif isinstance(recall_id_or_name, int):
                entries = [(key, value) for key, value in data.items()]
                if 1 <= recall_id_or_name <= len(entries):
                    return entries[recall_id_or_name-1][1]
            raise RecallNotFoundError(f"entry [cyan]{recall_id_or_name}[/cyan] not found in database.")
        except (DatabaseReadJsonError, DatabaseReadError) as e:
            self._logger.error(f"error: adding '{recall_id_or_name}' to recall index, {e}")
            raise RecallReadError(f"cannot read or invalid json in database.") from e

    def add(self, recall_name: str, recall_path: str) -> None:
        # Get the data from the database
        self._logger.info(f"Adding {recall_name} at {recall_path}.")
        try:
            data = self._db_handler.load()
            # assuming users has provided a recall_name and
            # reall_path that are correct. and cli interface has validated everything already
            # I am putting whatever user has provided directly to the database without validating if it's already present in the database.
            # check if the data exists
            if not (recall_name in data):
                data[recall_name] = recall_path  # should I do processing of text such as all lower case and such.
                self._db_handler.dump(data)
                return
            raise RecallExistsError(f"entry for [cyan]'{recall_name}'[/cyan] found in database.")
        except (DatabaseReadJsonError, DatabaseReadError) as e:
            self._logger.error(f"error: adding '{recall_name}' to recall index, {e}")
            raise RecallReadError(f"cannot read or invalid json in database.") from e
        except DatabaseWriteError as e:
            self._logger.error(f"error adding '{recall_name}' to database, {e}")
            raise RecallWriteError(f"cannot to write to database") from e

    def remove(self, recall_name: str) -> Tuple[str, str]:
        self._logger.info(f"Removing {recall_name} from index.")
        try:
            data = self._db_handler.load()
            entry = data.pop(recall_name)  # raise key error when no value is found
            self._db_handler.dump(data)
            return entry
        except KeyError as e:
            self._logger.error(f"error: '{recall_name}' not found in index")
            raise RecallNotFoundError(f"entry for [cyan]'{recall_name}'[/cyan] not found in database.") from e
        except (DatabaseReadJsonError, DatabaseReadError) as e:
            self._logger.error(f"error: removing '{recall_name}' from index, {e}")
            raise RecallReadError(f"cannot read or invalid json in database.") from e
        except DatabaseWriteError as e:
            self._logger.error(f"error removing '{recall_name}' from database, {e}")
            raise RecallWriteError(f"cannot write to database") from e

    def update(self, recall_name: str, recall_path: str) -> str:
        self._logger.info(f"Updating {recall_name} from index.")
        try:
            data = self._db_handler.load()
            if entry := data.get(recall_name):
                data[recall_name] = recall_path
                self._db_handler.dump(data)
                return entry
            raise RecallNotFoundError(f"entry for [cyan]'{recall_name}'[/cyan] not found in database.")
        except KeyError as e:
            self._logger.error(f"error: '{recall_name}' not found in index")
            raise RecallNotFoundError(f"entry for [cyan]'{recall_name}'[/cyan] not found in database.") from e
        except (DatabaseReadJsonError, DatabaseReadError) as e:
            self._logger.error(f"error: updating '{recall_name}' in index, {e}")
            raise RecallReadError(f"cannot read or invalid json in database.") from e
        except DatabaseWriteError as e:
            self._logger.error(f"error updating '{recall_name}' in database, {e}")
            raise RecallWriteError(f"cannot write to database") from e

    def show(self) -> Dict[str, Any]:
        self._logger.info(f"Fetching all entries")
        try:
            data = self._db_handler.load()
            return data
        except (DatabaseReadJsonError, DatabaseReadError) as e:
            self._logger.error(f"error: retrieving entries from index, {e}")
            raise RecallReadError(f"cannot read or invalid json in database.") from e


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
