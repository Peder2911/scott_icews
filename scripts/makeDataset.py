
import os
import re
import json
import pandas as pd

def getdict(path):
    with open(path) as f:
        return json.load(f)

targets,actions = (getdict(f"dictionaries/{nm}.json") for nm in ("targets","actions"))

dataframes = {"china":[],"us":[]}

for path in [p for p in os.listdir("icews") if re.search("^events.*tab$",p)]:
    data = pd.read_table(os.path.join("icews",path))

    usData = data[data["Source Name"].apply(lambda x: x in targets["china"])]
    usData = usData[usData["Target Name"].apply(lambda x: x in targets["us"])]
    dataframes["us"].append(usData)

    chinaData = data[data["Source Name"].apply(lambda x: x in targets["us"])]
    chinaData = chinaData[chinaData["Target Name"].apply(lambda x: x in targets["china"])]
    dataframes["china"].append(chinaData)

dataframes = {k:pd.concat(v) for k,v in dataframes.items()}

def classifyEvent(evt):
    if evt in actions["high"]:
        return "high"
    elif evt in actions["medium"]:
        return "medium"
    elif evt in actions["low"]:
        return "low"
    else:
        return pd.NA

for df in dataframes.values():
    df["event_class"] = df["Event Text"].apply(classifyEvent)

for k,v in dataframes.items():
    v.to_csv(f"out/{k}.csv")


