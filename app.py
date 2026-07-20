import streamlit as st
from llm import ask_ai


st.set_page_config(
    page_title="D <3 AI Assistant",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 D <3 AI Assistant")
st.caption("Your Personal AI Voice Assistant")


# Chat history initialize
if "messages" not in st.session_state:
    st.session_state.messages = []


# Show old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])



# User input
prompt = st.chat_input("Ask me anything...")


if prompt:

    # User message
    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )


    with st.chat_message("user"):
        st.write(prompt)



    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = ask_ai(prompt)

            st.write(response)


    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )