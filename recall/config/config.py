from pathlib import Path
from typing import Dict, Any, Optional

import tomllib
import tomli_w

from dataclasses import dataclass


APP_DIR = Path(__file__).home().resolve() / ".recall"

LOGS_DIR = APP_DIR / "logs"
CONFIG_DIR = APP_DIR / "config"
DATA_DIR = APP_DIR / "database"

DATABASE_FILE = DATA_DIR / "recall.json"
CONFIG_FILE = CONFIG_DIR / "config.toml"


DEFAULT_CONFIGURATION: Dict[str, Any] = {
    "app": {
        "init": False,
        "config": CONFIG_FILE.as_posix(),
        "database": DATABASE_FILE.as_posix(),
        "logs": LOGS_DIR.as_posix()

    },
}


@dataclass(frozen=True)
class Config:
    # remember we have not put all the FILES here as attribute cause that it will be static
    # and we want to read the values from the config file instead.
    APP_DIR: Path = APP_DIR
    CONFIG_DIR: Path = CONFIG_DIR
    DATA_DIR: Path = DATA_DIR
    CONFIG_FILE: Path = CONFIG_FILE

    @property
    def CONFIGURATION(self) -> Dict[str, Any]:
        # TODO: Add exception handling while reading the file
        try:
            with open(self.CONFIG_FILE, "rb") as file:
                return tomllib.load(file)
        except FileNotFoundError:
            return DEFAULT_CONFIGURATION

    @property
    def DATABASE_FILE(self) -> Path:
        # TODO: Add exception handling while reading the file
        return Path(self.CONFIGURATION["app"]["database"])
    
    @property
    def LOGS_DIR(self) -> Path:
        # TODO: Add exception handling while reading the file
        return Path(self.CONFIGURATION["app"]["logs"])
    
    @property
    def INITIALIZED(self) -> bool:
        # TODO: Add exception handling while reading the file
        return self.CONFIGURATION["app"].get("init", False)
    
    def init_config(self, db_file: Optional[Path], logs_dir: Optional[Path]) -> bool:
        
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.CONFIG_FILE.touch(exist_ok=True)
        
        database = db_file or DATABASE_FILE   # using self.DATABASE_FILE will cause very bad error cause it is not yet set
        logs = logs_dir or LOGS_DIR

        if database.exists() and database.is_dir():
            raise ValueError("Expected a file path got directory instead.")
        
        database.parent.mkdir(parents=True, exist_ok=True)
        logs.mkdir(parents=True, exist_ok=True)

        DEFAULT_CONFIGURATION["app"]["database"] = database.as_posix()
        DEFAULT_CONFIGURATION["app"]["logs"] = logs.as_posix()
        DEFAULT_CONFIGURATION["app"]["init"] = True

        with open(self.CONFIG_FILE, "wb") as file:
            tomli_w.dump(DEFAULT_CONFIGURATION, file)
        return True


config = Config()

