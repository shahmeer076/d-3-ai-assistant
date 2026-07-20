import json
import os


FILE = "web_chat_history.json"



def load_chats():

    if not os.path.exists(FILE):

        return {}


    try:

        with open(
            FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except (json.JSONDecodeError, FileNotFoundError):

        return {}




def save_chat(title, messages):

    chats = load_chats()


    chats[title] = messages


    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chats,
            f,
            indent=4,
            ensure_ascii=False
        )




def create_title(message):

    title = message.strip()


    if len(title) > 30:

        title = title[:30] + "..."


    return title