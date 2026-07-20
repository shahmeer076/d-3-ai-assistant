import json
import os


FILE = "chat_history.json"



def get_history():

    if not os.path.exists(FILE):

        return []


    try:

        with open(
            FILE,
            "r",
            encoding="utf-8"
        ) as f:

            chats = json.load(f)



        history = []


        for chat in chats:


            messages = chat.get(
                "messages",
                []
            )


            for msg in messages:


                if (
                    "role" in msg 
                    and 
                    "content" in msg
                ):

                    history.append(
                        {
                            "role":msg["role"],
                            "content":msg["content"]
                        }
                    )


        return history



    except:

        return []





def add_message(role, content):


    return