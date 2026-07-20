from groq import Groq
from chat_memory import get_history, add_message


from dotenv import load_dotenv
import os

load_dotenv()


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

Examples:

User:
What is Artificial Intelligence?

Assistant:
Artificial Intelligence is a branch of computer science that allows machines to learn, think and make decisions like humans.


User:
Artificial intelligence kya hoti hai?

Assistant:
Artificial intelligence aik technology hai jo machines ko data se seekhne aur decisions lene ki ability deti hai.


User:
How are you?

Assistant:
I am good! I am here to help you with your questions.


User:
kya haal hai?

Assistant:
Main theek hun 😊 aap batao, mein aapki kis cheez mein help kar sakta hun?

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