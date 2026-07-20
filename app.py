import streamlit as st

from text_to_speech import speak
from llm import ask_ai
from commands import run_command
from memory import save_memory, get_memory


st.set_page_config(
    page_title="Meeru AI Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Meeru AI Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []



for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])




user_input = st.chat_input(
    "Type your message..."
)



if user_input:


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    with st.chat_message("user"):

        st.markdown(user_input)



    text = user_input.lower()



    if "my name is" in text:


        name = text.replace(
            "my name is",
            ""
        ).strip()


        save_memory(
            "name",
            name
        )


        response = (
            f"Okay, I will remember your name {name}"
        )



    elif (
        "what is my name" in text
        or "who am i" in text
        or "what's my name" in text
    ):


        name = get_memory(
            "name"
        )


        if name == "I don't remember":

            response = (
                "I don't know your name yet"
            )

        else:

            response = (
                f"Your name is {name}"
            )



    else:


        command = run_command(
            user_input
        )


        if command:

            response = command


        else:

            response = ask_ai(
                user_input
            )



    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )



    with st.chat_message("assistant"):

        st.markdown(response)


        audio_file = speak(
            response
        )


        if audio_file:

            st.audio(
                audio_file,
                format="audio/mp3"
            )