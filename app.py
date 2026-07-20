import streamlit as st
from llm import ask_ai
from commands import run_command

from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components

import speech_recognition as sr
from pydub import AudioSegment
import io

from chat_history import load_chats, save_chat, delete_chats



# PAGE CONFIG

st.set_page_config(
    page_title="D <3 AI Assistant",
    page_icon="🤖",
    layout="wide"
)



# CSS

st.markdown(
"""
<style>

.stApp{
    background:#f8fafc;
}

h1{
    text-align:center;
    color:#2563eb;
}

section[data-testid="stSidebar"]{
    background:white;
}

.stButton button{
    width:100%;
    border-radius:20px;
}

</style>
""",
unsafe_allow_html=True
)





# HEADER

st.title("🤖 D <3 AI Assistant")

st.caption(
    "Your Personal AI Voice Assistant powered by Groq"
)





# SESSION

if "messages" not in st.session_state:

    st.session_state.messages=[]





# SIDEBAR

with st.sidebar:


    st.title("🤖 D <3 AI")


    st.write(
        "Your Intelligent Assistant"
    )


    st.divider()



    if st.button("➕ New Chat"):


        if st.session_state.messages:

            save_chat(
                st.session_state.messages
            )


        st.session_state.messages=[]

        st.rerun()





    if st.button("🗑 Clear Chats"):


        st.session_state.messages=[]

        delete_chats()

        st.rerun()




    st.divider()



    st.subheader("📚 History")


    chats=load_chats()



    if chats:


        for i,chat in enumerate(chats):


            title=chat.get(
                "title",
                "Chat"
            )


            if st.button(
                title,
                key=i
            ):


                st.session_state.messages = chat.get(
                    "messages",
                    []
                )


                st.rerun()


    else:

        st.info(
            "No chats saved"
        )



    st.divider()


    st.write(
"""
✨ Features

✅ AI Chat

✅ Voice Input

✅ Voice Output

✅ Memory

✅ Google Commands

✅ YouTube Commands

"""
    )







# SHOW OLD CHAT


for msg in st.session_state.messages:


    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )








# VOICE INPUT


st.subheader("🎤 Voice Assistant")



audio = mic_recorder(

    start_prompt="🎤 Start Speaking",

    stop_prompt="⏹ Stop Recording",

    just_once=True,

    use_container_width=True

)



voice_text=None




if audio:


    st.audio(
        audio["bytes"],
        format="audio/wav"
    )


    try:


        recognizer = sr.Recognizer()



        audio_file = io.BytesIO(
            audio["bytes"]
        )



        sound = AudioSegment.from_file(
            audio_file
        )



        sound.export(
            "voice.wav",
            format="wav"
        )



        with sr.AudioFile(
            "voice.wav"
        ) as source:


            audio_data = recognizer.record(
                source
            )



        voice_text = recognizer.recognize_google(
            audio_data
        )



        st.success(
            "You said: " + voice_text
        )



    except Exception as e:


        st.error(
            f"Voice Error: {e}"
        )







# TEXT INPUT


text_input = st.chat_input(
    "Type your message..."
)



prompt = voice_text or text_input







# PROCESS


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



            command = run_command(
                prompt
            )



            if command:


                response = command


            else:


                response = ask_ai(
                    prompt
                )





            st.write(response)






            # TEXT TO SPEECH


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



    save_chat(
        st.session_state.messages
    )