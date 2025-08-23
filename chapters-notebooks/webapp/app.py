import data_utils
import swimclub
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
    dates = [session[0].split(" ")[0] for session in data]
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
    file_id = request.form["file"]
    location = swimclub.produce_bar_chart(file_id, "templates/")
    return render_template(location.split("/")[-1])


if __name__ == "__main__":
    app.run(debug=True)
