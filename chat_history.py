import json
import os
from datetime import datetime


FILE_NAME = "chat_history.json"


def load_history():

    if not os.path.exists(FILE_NAME):
        return {}

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except:
        return {}



def save_chat(title, messages):

    history = load_history()

    history[title] = messages


    with open(FILE_NAME, "w") as file:
        json.dump(history, file, indent=4)



def get_history():

    return load_history()



def create_title():

    return "Chat " + datetime.now().strftime("%d-%m-%Y %I-%M-%S")



def delete_history():

    with open(FILE_NAME, "w") as file:
        json.dump({}, file)