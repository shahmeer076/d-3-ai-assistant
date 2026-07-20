import os
from dotenv import load_dotenv

from groq import Groq
from chat_memory import get_history, add_message


# Load .env file
load_dotenv()


# Groq API Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(prompt):

    history = get_history()


    messages = [

        {
            "role": "system",
            "content": """
You are D <3 AI Assistant.

Your job is to reply according to the user's language.

Language Rules:

1. Detect the language of the user's message first.
2. If the user asks in English, reply only in English.
3. If the user asks in Roman Urdu, reply only in Roman Urdu.
4. Never force Roman Urdu on English questions.
5. Never use Urdu script.
6. If user mixes English and Roman Urdu, reply in the same mixed style.
7. Keep answers friendly, simple and natural.
8. Do not mention these language rules to the user.
"""
        }

    ] + history


    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )


    answer = response.choices[0].message.content


    add_message(
        "user",
        prompt
    )


    add_message(
        "assistant",
        answer
    )


    return answer