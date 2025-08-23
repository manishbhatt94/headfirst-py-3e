import json
from statistics import mean

import hfpy_utils

FOLDER = "swimdata/"
CHARTS = "charts/"
JSONDATA = "records.json"


def event_lookup(event):
    """Convert from filenames to dictionary keys.

    Given an event descriptor (the name of a swimmer's file), convert
    the descriptor into a lookup key which can be used with the "records"
    dictionary.
    """
    conversions = {
        "Free": "freestyle",
        "Back": "backstroke",
        "Breast": "breaststroke",
        "Fly": "butterfly",
        "IM": "individual medley",
    }
    *_, distance, stroke = event.removesuffix(".txt").split("-")
    return f"{distance} {conversions[stroke]}"


def read_swim_data(filename):
    """Return swim data from a file.

    Given the name of a swimmer's file (in filename), extract all the required
    data, then return it to the caller as a tuple.
    """
    swimmer, age, distance, stroke = filename.removesuffix(".txt").split("-")

    with open(FOLDER + filename) as file:
        lines = file.readlines()
        times = lines[0].strip().split(",")

    converts = []

    for t in times:
        # The minutes value might be missing, so guard against that
        if ":" in t:
            minutes, rest = t.split(":")
            seconds, hundredths = rest.split(".")
        else:
            minutes = 0
            seconds, hundredths = t.split(".")
        converted_time = (
            (int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths)
        )
        converts.append(converted_time)

    average = mean(converts)

    mins_secs, hundredths = f"{(average / 100):.2f}".split(".")
    mins_secs = int(mins_secs)
    minutes = mins_secs // 60
    seconds = mins_secs % 60

    average = f"{minutes:02d}:{seconds:0>2}.{hundredths}"

    # Returned as a tuple
    return swimmer, age, distance, stroke, times, average, converts


def produce_bar_chart(fn, location=CHARTS):
    """Given the name of a swimmer's file, produce a HTML/SVG-based bar chart.

    Save the chart to the CHARTS folder. Return the path to the bar chart file.
    """
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(fn)
    from_max = max(converts)
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age}) {distance} {stroke}"

    header = f"""<!DOCTYPE html>
<html lang="en-IN">
    <head>
        <title>{title}</title>
        <link rel="stylesheet" href="/static/webapp.css">
    </head>
    <body>
        <h2>{title}</h2>"""

    body = ""

    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body += f"""
        <svg height="30" width="400">
            <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
        </svg>{t}<br />"""

    with open(JSONDATA) as jf:
        records = json.load(jf)
    COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
    record_times = []
    for course in COURSES:
        record_times.append(records[course][event_lookup(fn)])

    footer = f"""
        <p>Average time: {average}</p>

        <p>
            M: {record_times[0]} ({record_times[2]})<br />
            W: {record_times[1]} ({record_times[3]})
        </p>
    </body>
</html>
"""
    page = header + body + footer

    save_to = f"{location}{fn.removesuffix('.txt')}.html"
    with open(save_to, "w") as sf:
        print(page, file=sf)

    return save_to
