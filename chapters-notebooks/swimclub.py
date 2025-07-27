from statistics import mean

FOLDER = "../swimdata/"


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

    mins_secs, hundredths = str(round(average / 100, 2)).split(".")
    mins_secs = int(mins_secs)
    hundredths = int(hundredths)
    minutes = mins_secs // 60
    seconds = mins_secs % 60

    average = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"

    return swimmer, age, distance, stroke, times, average  # Returned as a tuple
