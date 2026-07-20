import json
import os
from datetime import datetime


FILE = "chat_history.json"



def load_chats():

    if not os.path.exists(FILE):

        return []


    try:

        with open(FILE, "r", encoding="utf-8") as f:

            chats = json.load(f)


        return chats


    except:

        return []





def save_chat(messages):


    chats = load_chats()



    title = "New Chat"


    for msg in messages:

        if msg["role"] == "user":

            title = msg["content"][:30]

            break




    chat = {

        "title": title,

        "time": str(datetime.now()),

        "messages": messages

    }




    chats.append(chat)



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





def delete_chats():

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            [],
            f
        )