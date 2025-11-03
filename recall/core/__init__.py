from recall.core.manager import Recall


from recall.config import config
from recall.core.database.manager import DatabaseHandler
from recall.core.database import get_database_path
# from recall import __app_name__, __version__, recall, database,ERRORS, config

# from recall.core import get_database_path


class RecallConfigInitException(Exception):
    pass

class RecallDatabaseInitException(Exception):
    pass




def get_database_handler():
    global _db_handler
    try:
        db_path = get_database_path(config)
        _db_handler = DatabaseHandler(db_path)
        return _db_handler
    except Exception as e:
        raise(RecallDatabaseInitException(e))
    
   

def get_recaller() -> Recall:
    if config.INITIALIZED:
        db_path = get_database_path(config)
        if db_path.exists():
            return Recall(db_path)
        else:
            print('Database not found Please run recall init')
            raise(RecallDatabaseInitException("no database"))
    else:
        print('Config file not found Please run recall init')
        raise(RecallConfigInitException('No config file'))



