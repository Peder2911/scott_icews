
import json
import functools
import pandas as pd

targets = {"us":[],"china":[]}

dictionary = {k:pd.read_excel(f"coded/China_Intensity_{k.title()}.xlsx") for k in ["high","medium","low"]}

setof = lambda c: functools.reduce(lambda x,y: x.union(y),[set(ds[c]) for ds in dictionary.values()])

targets["china"] = list(setof("Source_Name"))
targets["us"] = list(setof("Target_Name"))
actions = {k:list(set(v["Event_Text"])) for k,v in dictionary.items()}

with open("dictionaries/targets.json","w") as f:
    json.dump(targets,f)
with open("dictionaries/actions.json","w") as f:
    json.dump(actions,f)


