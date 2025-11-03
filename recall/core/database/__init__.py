from pathlib import Path
from typing import Dict, Any

from recall import DB_WRITE_ERROR, SUCCESS


def init_database(database_path: Path) -> int:
    try:
        database_path.write_text('[]')
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


def get_database_path(config: Dict[str, Any]) -> Path:
    return Path(config.DATABASE_FILE)
