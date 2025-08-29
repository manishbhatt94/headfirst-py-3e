import DBcm
import queries


class DataUtilsDbCm:
    def __init__(self, db_details):
        self.db_details = db_details

    def get_swim_sessions(self):
        """Return a tuple-list of unique session timestamps."""
        with DBcm.UseDatabase(self.db_details) as db:
            db.execute(queries.SQL_SESSIONS)
            results = db.fetchall()
        return results

    def get_session_swimmers(self, date):
        """When given a date (YYYY-MM-DD), return a tuple-list of swimmers
        and their associated age (filtered by date).
        """
        with DBcm.UseDatabase(self.db_details) as db:
            db.execute(queries.SQL_SWIMMERS_BY_SESSION, (date,))
            results = db.fetchall()
        return results

    def get_swimmers_events(self, name, age, date):
        """When given a date (YYYY-DD-MM), swimmer's name, and swimmer's age, return
        a tuple-list of events the swimmer swam on that date."""
        with DBcm.UseDatabase(self.db_details) as db:
            db.execute(
                queries.SQL_SWIMMERS_EVENTS_BY_SESSION,
                (
                    name,
                    age,
                    date,
                ),
            )
            results = db.fetchall()
        return results

    def get_swimmers_times(self, name, age, distance, stroke, date):
        """When given a swimmer's name, swimmer's age group, distance, stroke, and
        a swim session date (YYYY-MM-DD), return a tuple-list of times the swimmer
        swam on that date over the identified distance/stroke combination."""
        with DBcm.UseDatabase(self.db_details) as db:
            db.execute(
                queries.SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION,
                (
                    name,
                    age,
                    distance,
                    stroke,
                    date,
                ),
            )
            results = db.fetchall()
        return results
