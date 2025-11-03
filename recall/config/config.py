from pathlib import Path
from typing import Dict, Any, Optional

import tomllib
import tomli_w

from dataclasses import dataclass


APP_DIR = Path(__file__).resolve().parent.parent


LOG_DIR = APP_DIR / "logs"
CONFIG_DIR = APP_DIR / "config"
DATA_DIR = APP_DIR / "data"

DATABASE_FILE = DATA_DIR / "recall.json"
CONFIG_FILE = CONFIG_DIR / "config.toml"


DEFAULT_CONFIGURATION: Dict[str, Any] = {
    "app": {
        "init": False,
        "database": DATABASE_FILE.as_posix(),
        "logs": LOG_DIR.as_posix()
    },
}


@dataclass(frozen=True)
class Config:
    
    APP_DIR: Path = APP_DIR
    CONFIG_DIR: Path = CONFIG_DIR
    DATA_DIR: Path = DATA_DIR
    CONFIG_FILE = CONFIG_FILE

    @property
    def CONFIGURATION(self) -> Dict[str, Any]:
        # TODO: Add exception handling while reading the file
        try:
            with open(self.CONFIG_FILE, "rb") as file:
                return tomllib.load(file)
        except FileNotFoundError:
            return DEFAULT_CONFIGURATION

    @property
    def DATABASE_FILE(self) -> str:
        # TODO: Add exception handling while reading the file
        return self.CONFIGURATION["app"]["database"]
    
    @property
    def LOG_DIR(self) -> Path:
        # TODO: Add exception handling while reading the file
        return self.CONFIGURATION["app"]["logs"]
    
    @property
    def INITIALIZED(self) -> bool:
        # TODO: Add exception handling while reading the file
        return self.CONFIGURATION["app"].get("init", False)
    
    def init_config(self, db_path: Optional[Path], log_path: Optional[Path]) -> bool:
        
        # self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.CONFIG_FILE.touch(exist_ok=True)
        
        database = db_path or DATABASE_FILE
        log = log_path or LOG_DIR

        if database.exists() and database.is_dir():
            raise ValueError("Expected a file path got directory instead.")
        
        database.parent.mkdir(parents=True, exist_ok=True)
        log.mkdir(parents=True, exist_ok=True)

        DEFAULT_CONFIGURATION["app"]["database"] = database.as_posix()
        DEFAULT_CONFIGURATION["app"]["logs"] = log.as_posix()
        DEFAULT_CONFIGURATION["app"]["init"] = True

        with open(CONFIG_FILE, "wb") as file:
            tomli_w.dump(DEFAULT_CONFIGURATION, file)
        return True


config = Config()
