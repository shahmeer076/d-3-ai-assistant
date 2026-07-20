import json
import os
from datetime import datetime


FILE = "web_chat_history.json"



def load_chats():

    if not os.path.exists(FILE):

        return {}


    try:

        with open(FILE,"r") as f:

            return json.load(f)


    except:

        return {}




def save_chat(title,messages):


    chats = load_chats()


    chats[title]=messages


    with open(FILE,"w") as f:

        json.dump(
            chats,
            f,
            indent=4
        )




def create_title(message):


    title = message.strip()



    # Title length limit

    if len(title) > 30:

        title = title[:30] + "..."



    return title