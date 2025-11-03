import json
from typing import Dict, NamedTuple, List
from pathlib import Path
from recall import DB_READ_ERROR, DB_WRITE_ERROR, SUCCESS, JSON_ERROR


class DBResponse(NamedTuple):
    database: List[Dict[str, str]]
    error: int


class DatabaseHandler:

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def read(self) -> DBResponse:
        try:
            with open(self.database_path, mode='r', encoding='utf-8') as file:
                content = json.load(file)
        except json.decoder.JSONDecodeError:
            return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)
        return DBResponse(content, SUCCESS)


    def write(self, recalls: List[Dict[str, str]]) -> DBResponse:
        try:
            with open(self.database_path, mode='w', encoding='utf-8') as file:
                json.dump(recalls, file, indent=4)
        except OSError:
            return DBResponse(recalls, DB_WRITE_ERROR)
        return DBResponse(recalls, SUCCESS)
