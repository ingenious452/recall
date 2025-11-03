__app_name__ = "recall"
__version__ = "0.2.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    PROJECT_ID_ERROR,
    PROJECT_DIR_ERROR,
) = range(8)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    PROJECT_ID_ERROR: "project name error",
    PROJECT_DIR_ERROR: "project directory error"
}
