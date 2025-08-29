import pymysql
import queries


class DataUtilsPyMySQL:
    def __init__(self, db_details):
        """
        db_details: dict containing connection info, e.g.:
            {
                'host': 'localhost',
                'user': 'username',
                'password': 'password',
                'database': 'dbname',
                'port': 3306,  # optional, defaults to 3306
                'charset': 'utf8mb4'  # optional
            }
        """
        self.db_details = db_details

    def _get_connection(self):
        """Create and return a new PyMySQL connection."""
        return pymysql.connect(
            host=self.db_details["host"],
            user=self.db_details["user"],
            password=self.db_details["password"],
            database=self.db_details["database"],
            port=self.db_details.get("port", 3306),
            charset=self.db_details.get("charset", "utf8mb4"),
            cursorclass=pymysql.cursors.DictCursor,
        )

    def get_swim_sessions(self):
        """Return a tuple-list of unique session timestamps."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.SQL_SESSIONS)
                results = cur.fetchall()
        results = [(result["ts"],) for result in results]
        return results

    def get_session_swimmers(self, date):
        """Return list of swimmers + age for a given session date."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.SQL_SWIMMERS_BY_SESSION, (date,))
                results = cur.fetchall()
        results = [(result["name"], result["age"]) for result in results]
        return results

    def get_swimmers_events(self, name, age, date):
        """Return events swum by a specific swimmer on a given date."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.SQL_SWIMMERS_EVENTS_BY_SESSION, (name, age, date))
                results = cur.fetchall()
        results = [(result["distance"], result["stroke"]) for result in results]
        return results

    def get_swimmers_times(self, name, age, distance, stroke, date):
        """Return times for a swimmer's distance/stroke in a session."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    queries.SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION,
                    (name, age, distance, stroke, date),
                )
                results = cur.fetchall()
        results = [(result["time"],) for result in results]
        return results
