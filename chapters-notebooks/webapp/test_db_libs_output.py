from dbcm_data_utils import DataUtilsDbCm
from pymysql_data_utils import DataUtilsPyMySQL

db_details = {
    "host": "127.0.0.1",
    "database": "swimDB",
    "user": "swimuser",
    "password": "swimpasswd",
}


def test_get_swim_sessions():
    dbcm_result = DataUtilsDbCm(db_details).get_swim_sessions()
    pymysql_result = DataUtilsPyMySQL(db_details).get_swim_sessions()
    assert dbcm_result == pymysql_result


def test_get_session_swimmers():
    dbcm_result = DataUtilsDbCm(db_details).get_session_swimmers("2025-08-22")
    pymysql_result = DataUtilsPyMySQL(db_details).get_session_swimmers("2025-08-22")
    assert dbcm_result == pymysql_result


def test_get_swimmers_events():
    dbcm_result = DataUtilsDbCm(db_details).get_swimmers_events(
        "Darius", 8, "2025-08-22"
    )
    pymysql_result = DataUtilsPyMySQL(db_details).get_swimmers_events(
        "Darius", 8, "2025-08-22"
    )
    assert dbcm_result == pymysql_result


def test_get_swimmers_times():
    dbcm_result = DataUtilsDbCm(db_details).get_swimmers_times(
        "Darius", 8, "50m", "Free", "2025-08-22"
    )
    pymysql_result = DataUtilsPyMySQL(db_details).get_swimmers_times(
        "Darius", 8, "50m", "Free", "2025-08-22"
    )
    assert dbcm_result == pymysql_result
