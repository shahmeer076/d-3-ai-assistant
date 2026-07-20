import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from flask import Flask, render_template, request, jsonify

from llm import ask_ai
from commands import run_command
from memory import save_memory, get_memory

from chat_storage import save_chat, create_title, load_chats


app = Flask(__name__)


current_chat = None
messages = []


# Home page
@app.route("/")
def home():

    return render_template("index.html")



# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    global messages, current_chat


    user_message = request.json["message"]


    text = user_message.lower()


    if current_chat is None:

        current_chat = create_title(user_message)



    # Memory system

    if "my name is" in text:


        name = text.replace(
            "my name is",
            ""
        ).strip()


        save_memory(
            "name",
            name
        )


        response = f"I will remember your name {name}"



    elif "what is my name" in text or "who am i" in text:


        name = get_memory("name")


        if name:

            response = f"Your name is {name}"


        else:

            response = "I don't know your name yet"



    else:


        command = run_command(user_message)


        if command:

            response = command


        else:

            response = ask_ai(user_message)



    # Save Chat History

    messages.append(
        {
            "sender": "You",
            "message": user_message
        }
    )


    messages.append(
        {
            "sender": "AI",
            "message": response
        }
    )


    save_chat(
        current_chat,
        messages
    )


    return jsonify(
        {
            "reply": response
        }
    )



# History API

@app.route("/history")
def history():

    return jsonify(
        load_chats()
    )




if __name__ == "__main__":

    app.run(debug=True)