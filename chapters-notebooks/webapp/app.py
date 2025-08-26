import convert_utils
import data_utils
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "463c4898bcf3ed83fd13cf48d360e4cdb577cae2058b7215b8bdabeac4c34194"


@app.get("/")
def index():
    return render_template(
        "index.html",
        title="Welcome to the Swimclub",
    )


@app.get("/swims")
def display_swim_sessions():
    data = data_utils.get_swim_sessions()
    ## dates = [session[0].split(" ")[0] for session in data]   # SQLite3.
    dates = [str(session[0].date()) for session in data]  # MariaDB.
    # MariaDB's python driver returns Python `datetime` objects. So we convert
    # those to strings.
    # Whereas, SQLite3's python driver returned plain date time strings.
    return render_template(
        "select.html",
        title="Select a swim session",
        url="/swimmers",
        select_id="chosen_date",
        data=dates,
    )


@app.post("/swimmers")
def display_swimmers():
    session["chosen_date"] = request.form["chosen_date"]
    data = data_utils.get_session_swimmers(session["chosen_date"])
    swimmers = [f"{name}-{age}" for name, age in data]
    return render_template(
        "select.html",
        title="Select a swimmer",
        url="/showevents",
        select_id="swimmer",
        data=sorted(swimmers),
    )


@app.post("/showevents")
def display_swimmer_events():
    session["swimmer"], session["age"] = request.form["swimmer"].split("-")
    data = data_utils.get_swimmers_events(
        session["swimmer"], session["age"], session["chosen_date"]
    )
    events = [f"{distance} {stroke}" for distance, stroke in data]
    return render_template(
        "select.html",
        title="Select an event",
        url="/showbarchart",
        select_id="event",
        data=events,
    )


@app.post("/showbarchart")
def show_bar_chart():
    distance, stroke = request.form["event"].split(" ")
    data = data_utils.get_swimmers_times(
        session["swimmer"], session["age"], distance, stroke, session["chosen_date"]
    )
    times = [time[0] for time in data]
    average_str, times_reversed, scaled = convert_utils.perform_conversions(times)
    world_records = convert_utils.get_worlds(distance, stroke)
    header = f"{session['swimmer']} (Under {session['age']}) {distance} {stroke} - {session['chosen_date']}"

    return render_template(
        "chart.html",
        title=header,
        data=list(zip(times_reversed, scaled)),
        average=average_str,
        worlds=world_records,
    )


if __name__ == "__main__":
    app.run(debug=True)
