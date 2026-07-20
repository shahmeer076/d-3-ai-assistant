import streamlit as st
from llm import ask_ai
from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components
import speech_recognition as sr


# Page Configuration
st.set_page_config(
    page_title="D <3 AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# Custom CSS
st.markdown(
    """
    <style>

    .stApp {
        background-color:#f8fafc;
    }


    h1 {
        text-align:center;
        color:#2563eb;
    }


    .stChatMessage {

        border-radius:15px;
        padding:10px;

    }


    section[data-testid="stSidebar"] {

        background-color:#ffffff;

    }


    .stButton button {

        width:100%;
        border-radius:20px;
        height:40px;

    }

    </style>

    """,
    unsafe_allow_html=True
)



# Header

st.title("🤖 D <3 AI Assistant")

st.caption(
    "Your Personal AI Voice Assistant powered by Groq LLM"
)



# Session Memory

if "messages" not in st.session_state:

    st.session_state.messages = []



# Sidebar

with st.sidebar:


    st.title("🤖 D <3 AI")


    st.write(
        "Your intelligent voice companion"
    )


    st.divider()



    if st.button("➕ New Chat"):

        st.session_state.messages = []

        st.rerun()



    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()



    st.divider()


    st.subheader("✨ Features")

    st.write(
        """
        ✅ AI Chat  
        ✅ Voice Input  
        ✅ Voice Output  
        ✅ Memory System  
        ✅ Groq LLM  
        """
    )


    st.divider()


    st.subheader("About")

    st.write(
        """
        D <3 AI Assistant is an AI
        powered personal assistant
        built using:

        • Python
        • Streamlit
        • Groq LLM
        • Speech Recognition
        """
    )



# Previous Chat Messages

for message in st.session_state.messages:


    with st.chat_message(message["role"]):

        st.write(message["content"])





# Voice Input

st.subheader("🎤 Voice Assistant")


audio = mic_recorder(

    start_prompt="🎤 Start Speaking",

    stop_prompt="⏹ Stop",

    just_once=True,

    use_container_width=True

)



voice_prompt = None



if audio:


    st.audio(audio["bytes"])


    try:


        with open(
            "voice.wav",
            "wb"
        ) as file:

            file.write(
                audio["bytes"]
            )



        recognizer = sr.Recognizer()



        with sr.AudioFile(
            "voice.wav"
        ) as source:


            audio_data = recognizer.record(
                source
            )



        voice_prompt = recognizer.recognize_google(
            audio_data
        )



        st.success(
            f"You said: {voice_prompt}"
        )



    except:


        st.error(
            "Voice could not be recognized"
        )





# Text Input

text_prompt = st.chat_input(
    "Type your message..."
)



prompt = voice_prompt or text_prompt





# AI Processing

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


        with st.spinner(
            "D <3 is thinking..."
        ):


            response = ask_ai(prompt)



            st.write(response)




            # Voice Output

            components.html(

                f"""

                <script>


                let speech = new SpeechSynthesisUtterance(

                    `{response}`

                );


                speech.lang="en-US";


                window.speechSynthesis.speak(
                    speech
                );


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