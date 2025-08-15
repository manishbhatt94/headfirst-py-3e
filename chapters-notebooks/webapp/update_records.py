import json

import gazpacho

URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"

# Indices of tables in the Wikipedia page which contain the world records data
RECORDS = (0, 1, 3, 4)

# LC -> Long Course (Swimming in a 50m pool)
# SC -> Short Course (Swimming in a 25m pool)
COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")

# WHERE = ""  # for running locally
WHERE = "/home/mangoeseverywhere/webapp/"  # for running on PythonAnywhere
JSONDATA = "records.json"

html = gazpacho.get(URL)
soup = gazpacho.Soup(html)
tables = soup.find("table")
records = {}
for table, course in zip(RECORDS, COURSES):
    records[course] = {}
    for row in tables[table].find("tr")[1:]:
        columns = row.find("td")
        event = columns[0].text
        time = columns[1].text
        if "relay" not in event:
            records[course][event] = time
with open(WHERE + JSONDATA, "w") as jf:
    json.dump(records, jf)
