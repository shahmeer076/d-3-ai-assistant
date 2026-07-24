import json
import os


MEMORY_FILE = "memory.json"



def get_memory():

    if not os.path.exists(MEMORY_FILE):

        return {}


    with open(
        MEMORY_FILE,
        "r"
    ) as file:

        return json.load(file)




def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4
        )




def add_memory(key, value):

    memory = get_memory()


    memory[key] = value


    save_memory(memory)