import platform

from dbcm_data_utils import DataUtilsDbCm
from pymysql_data_utils import DataUtilsPyMySQL

# SQLite specific DBcm database config variable (just a str with DB filename)
## db_details = "CoachDB.sqlite3"

# MariaDB specific DBcm database config variable - dict containing information
# about the DB connection and credentials

if "aws" in platform.uname().release:
    # Running on PythonAnywhere.
    db_details = {
        "host": "mangoeseverywhere.mysql.pythonanywhere-services.com",
        "database": "mangoeseverywher$default",
        "user": "mangoeseverywher",
        "password": "swimpasswd",
    }
    data_utils_obj = DataUtilsPyMySQL(db_details)
else:
    # Running locally.
    db_details = {
        # "localhost" as host doesn't work when DB is running within docker.
        # Instead "127.0.0.1" works fine!
        ## "host": "localhost",
        "host": "127.0.0.1",
        "database": "swimDB",
        "user": "swimuser",
        "password": "swimpasswd",
    }
    data_utils_obj = DataUtilsDbCm(db_details)


def get_swim_sessions():
    """Return a tuple-list of unique session timestamps."""
    return data_utils_obj.get_swim_sessions()


def get_session_swimmers(date):
    """When given a date (YYYY-MM-DD), return a tuple-list of swimmers
    and their associated age (filtered by date).
    """
    return data_utils_obj.get_session_swimmers(date)


def get_swimmers_events(name, age, date):
    """When given a date (YYYY-DD-MM), swimmer's name, and swimmer's age, return
    a tuple-list of events the swimmer swam on that date."""
    return data_utils_obj.get_swimmers_events(name, age, date)


def get_swimmers_times(name, age, distance, stroke, date):
    """When given a swimmer's name, swimmer's age group, distance, stroke, and
    a swim session date (YYYY-MM-DD), return a tuple-list of times the swimmer
    swam on that date over the identified distance/stroke combination."""
    return data_utils_obj.get_swimmers_times(name, age, distance, stroke, date)
