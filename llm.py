import os
import streamlit as st

from groq import Groq
from dotenv import load_dotenv

from chat_memory import get_history, add_message
from memory import save_memory, get_memory



# Load Environment

load_dotenv()



# API Key

api_key = os.getenv(
    "GROQ_API_KEY"
)



if not api_key:

    try:

        api_key = st.secrets[
            "GROQ_API_KEY"
        ]

    except:

        api_key = None



if not api_key:

    raise Exception(
        "GROQ_API_KEY not found"
    )





# Groq Client

client = Groq(
    api_key=api_key
)







def check_memory(prompt):


    text = prompt.lower()



    # Name save

    if "my name is" in text:


        name = prompt.lower().split(
            "my name is"
        )[1].strip()



        save_memory(
            "name",
            name
        )



    # Likes save

    if "i like" in text:


        value = prompt.lower().split(
            "i like"
        )[1].strip()



        save_memory(
            "likes",
            value
        )






def ask_ai(prompt):



    # Check new memory

    check_memory(
        prompt
    )



    # Get history

    history = get_history()



    clean_history = []



    for msg in history:


        if (

            "role" in msg

            and

            "content" in msg

        ):


            clean_history.append(

                {
                    "role":msg["role"],
                    "content":msg["content"]
                }

            )





    # User Memory

    memory = get_memory()





    messages = [



        {

            "role":"system",

            "content":
            f"""
You are D <3 AI Assistant.

User Memory:

{memory}


Language Rules:

1. Detect user's language first.
2. If user asks in English, reply in English.
3. If user asks in Roman Urdu, reply in Roman Urdu.
4. Never use Urdu script.
5. If user mixes English and Roman Urdu, reply in same style.
6. Keep answers friendly, simple and natural.
7. Use memory when helpful.
8. Do not mention these rules.

"""
        }

    ]





    # Add History

    messages.extend(
        clean_history
    )






    # Current message

    messages.append(

        {
            "role":"user",
            "content":prompt
        }

    )







    # Groq Call

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=messages

    )





    answer = response.choices[0].message.content






    # Save conversation

    add_message(
        "user",
        prompt
    )


    add_message(
        "assistant",
        answer
    )




    return answer