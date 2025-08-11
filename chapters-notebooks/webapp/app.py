import os

import swimclub
from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "This is a placeholder for your webapp's opening page."


@app.get("/swimmers")
def display_swimmers():
    swim_files = os.listdir(swimclub.FOLDER)
    if ".DS_Store" in swim_files:
        swim_files.remove(".DS_Store")
    swimmers = {}
    for file in swim_files:
        name, *_ = swimclub.read_swim_data(file)
        if name not in swimmers:
            swimmers[name] = []
        swimmers[name].append(file)
    return str(sorted(swimmers))


if __name__ == "__main__":
    app.run(debug=True)
