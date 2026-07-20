import streamlit as st
from llm import ask_ai
from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components
import base64


st.set_page_config(
    page_title="D <3 AI Assistant",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 D <3 AI Assistant")
st.caption("Your Personal AI Voice Assistant")


# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# Previous messages show
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])



st.markdown("### 🎤 Speak")


audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True,
    use_container_width=True
)


prompt = None


if audio:

    st.audio(audio["bytes"])


    # Voice input ke liye abhi placeholder
    st.info("Voice received. Speech-to-text processing add karenge.")



prompt = st.chat_input("Ask me anything...")



if prompt:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )


    with st.chat_message("user"):
        st.write(prompt)



    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = ask_ai(prompt)


            st.write(response)



            # Browser voice
            components.html(
                f"""
                <script>

                var msg = new SpeechSynthesisUtterance(
                    `{response}`
                );

                msg.lang="en-US";

                window.speechSynthesis.speak(msg);

                </script>
                """,
                height=0
            )



    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )