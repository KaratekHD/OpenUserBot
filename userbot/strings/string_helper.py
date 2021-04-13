
import json
import os
import random


# get string from json file
def get_string(module: str, name: str, lang: str):
    try:
        if not os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + "/" + lang + "/" + module + ".json"):
            lang = "en"
        with open(os.path.dirname(os.path.abspath(__file__)) + "/" + lang + "/" + module + ".json") as f:
            data = json.load(f)
        return data[name]
    except FileNotFoundError as excp:
        return excp.__cause__
    except KeyError as e:
        return e.__cause__




# for /runs, /slap etc.
def get_random_string(module: str, lang: str):
    if not os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + "/" + lang + "/" + module + ".json"):
        lang = "en"
    with open(os.path.dirname(os.path.abspath(__file__)) + "/" + lang + "/" + module + ".json") as f:
        data = json.load(f)
    i = len(data)
    r = str(random.randint(1, i))
    return data[r]