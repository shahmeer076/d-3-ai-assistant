import streamlit as st


st.set_page_config(
    page_title="D <3",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 D <3 AI")


st.write("AI Assistant")


message = st.chat_input(
    "Type your message..."
)


if message:


    st.chat_message("user").write(message)


    st.chat_message("assistant").write(
        "Hello Shahmeer 👋 Streamlit is working!"
    )