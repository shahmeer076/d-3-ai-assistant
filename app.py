import streamlit as st
from llm import ask_ai
from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components
import speech_recognition as sr


# Page Setup
st.set_page_config(
    page_title="D <3 AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# Title
st.title("🤖 D <3 AI Assistant")
st.caption("Your Personal AI Voice Assistant")


# Sidebar
with st.sidebar:

    st.header("⚙️ Settings")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()


    st.write("AI Assistant powered by Groq")


# Chat memory
if "messages" not in st.session_state:

    st.session_state.messages = []



# Show previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])



# Voice Section

st.markdown("## 🎤 Voice Assistant")


audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True,
    use_container_width=True
)



voice_prompt = None



if audio:


    st.audio(audio["bytes"])


    try:


        with open("voice.wav", "wb") as f:

            f.write(audio["bytes"])



        recognizer = sr.Recognizer()



        with sr.AudioFile("voice.wav") as source:

            audio_data = recognizer.record(source)



        voice_prompt = recognizer.recognize_google(audio_data)



        st.success(
            f"You said: {voice_prompt}"
        )



    except Exception as e:

        st.error(
            "Sorry, I could not understand your voice."
        )



# Text Input

text_prompt = st.chat_input(
    "Ask me anything..."
)



# Choose input source

prompt = voice_prompt or text_prompt



if prompt:


    # Save user message

    st.session_state.messages.append(

        {
            "role": "user",
            "content": prompt
        }

    )



    with st.chat_message("user"):

        st.write(prompt)




    # AI Response

    with st.chat_message("assistant"):


        with st.spinner("Thinking..."):


            response = ask_ai(prompt)



            st.write(response)



            # Text To Speech

            components.html(

                f"""

                <script>


                var msg = new SpeechSynthesisUtterance(

                    `{response}`

                );


                msg.lang = "en-US";


                window.speechSynthesis.speak(msg);



                </script>

                """,

                height=0

            )




    # Save AI response

    st.session_state.messages.append(

        {
            "role": "assistant",
            "content": response
        }

    )