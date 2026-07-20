import json
import os


FILE = "memory.json"


def load_memory():

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except:
        return {}



def save_memory(key, value):

    memory = load_memory()

    memory[key] = value

    with open(FILE, "w") as f:
        json.dump(
            memory,
            f,
            indent=4
        )



def get_memory(key):

    memory = load_memory()

    return memory.get(
        key,
        "I don't remember"
    )