from typing import Any

class BaseDatabaseError(Exception):
    def __init__(self, err_msg: str):
        super().__init__(err_msg)


class DatabaseReadError(BaseDatabaseError):
    pass

class DatabaseWriteError(BaseDatabaseError):
    pass

class DatabaseReadJsonError(DatabaseReadError):
    pass

class DatabaseNotFoundError(BaseDatabaseError):
    pass

class InitializationError(Exception):
    def __init__(self, e: Any):
        super().__init__(self, e)


class DatabaseInitializationError(InitializationError):
    pass


class ConfigNotFoundError(InitializationError):
    pass


class BaseRecallError(Exception):
    def __init__(self, err_msg: str):
        super().__init__(err_msg)


class RecallInitError(BaseRecallError):
    pass

class RecallNotFoundError(BaseRecallError):
    pass

class RecallReadError(BaseRecallError):
    pass

class RecallWriteError(BaseRecallError):
    pass

class RecallExistsError(BaseRecallError):
    pass


