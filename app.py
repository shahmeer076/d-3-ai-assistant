import streamlit as st
from llm import ask_ai
from commands import run_command
import streamlit.components.v1 as components

from chat_history import load_chats, save_chat, delete_chats
from memory import get_memory, add_memory


st.set_page_config(
    page_title="D <3 AI",
    page_icon="🤖",
    layout="wide"
)


# ================= CSS =================

st.markdown("""
<style>

.stApp{
    background:#ffffff;
}


section[data-testid="stSidebar"]{
    background:#0057B8;
}


section[data-testid="stSidebar"] *{
    color:white !important;
}


/* Buttons */

.stButton button{

    background:linear-gradient(
    135deg,
    #0057B8,
    #E31E24
    );

    color:white;

    border:none;

    border-radius:25px;

    font-weight:bold;

}


/* Chat Input */

div[data-testid="stChatInput"]{

    border-radius:30px !important;

    background:white !important;

    box-shadow:
    0px 5px 20px rgba(0,0,0,0.15);

}


div[data-testid="stChatInput"] textarea{

    border:none !important;

}



/* Messages */

div[data-testid="stChatMessage"]{

    border-radius:20px;

    padding:15px;

}


</style>
""",
unsafe_allow_html=True)



# ================= HEADER =================


st.markdown("""
<div style="
background:linear-gradient(135deg,#0057B8,#E31E24);
padding:30px;
border-radius:25px;
text-align:center;
color:white;
">

<h1 style="color:white;">
🤖 D <3 AI
</h1>

<p>
Your Personal AI Voice Assistant
</p>

<b>
🟢 ONLINE
</b>

</div>

""",
unsafe_allow_html=True)



# ================= SESSION =================


if "messages" not in st.session_state:

    st.session_state.messages=[]



# ================= SIDEBAR =================


with st.sidebar:


    st.markdown("""
<h1 style="color:white;">
🤖 D <3 AI
</h1>

<p>
Intelligent Voice Assistant
</p>
""",
unsafe_allow_html=True)



    if st.button("➕ New Chat"):


        if st.session_state.messages:

            save_chat(
                st.session_state.messages
            )


        st.session_state.messages=[]

        st.rerun()



    if st.button("🗑 Delete History"):


        delete_chats()

        st.session_state.messages=[]

        st.rerun()



    st.subheader("📚 Chat History")


    chats=load_chats()


    for i,chat in enumerate(chats):


        title=chat.get(
            "title",
            f"Chat {i+1}"
        )


        if st.button(
            title,
            key=f"chat_{i}"
        ):


            st.session_state.messages = chat.get(
                "messages",
                []
            )

            st.rerun()



    st.divider()


    st.write("""
✨ Features

🤖 AI Intelligence

💾 Memory

🌐 Commands

⚡ Fast Response
""")





# ================= CHAT DISPLAY =================


for msg in st.session_state.messages:


    avatar = (
        "👤"
        if msg["role"]=="user"
        else
        "🤖"
    )


    with st.chat_message(
        msg["role"],
        avatar=avatar
    ):

        st.write(
            msg["content"]
        )





# ================= INPUT =================


prompt = st.chat_input(
    "Ask D <3 anything..."
)




# ================= AI =================


if prompt:



    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )



    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(prompt)





    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):


        with st.spinner(
            "🤖 D <3 is thinking..."
        ):



            command = run_command(prompt)



            if command:

                response = command


            else:


                memory = get_memory()



                response = ask_ai(
f"""
You are D <3 AI Assistant.

User Memory:

{memory}


User Message:

{prompt}


Reply naturally.
"""
                )



            st.write(response)





            # Text To Speech

            safe=response.replace(
                "`",
                ""
            )


            components.html(
f"""

<script>

let speech =
new SpeechSynthesisUtterance(
`{safe}`
);


speech.lang="en-US";

speech.rate=0.9;


window.speechSynthesis.speak(
speech
);


</script>

""",
height=0
)




    # MEMORY SAVE


    if "my name is" in prompt.lower():


        name = prompt.lower().replace(
            "my name is",
            ""
        ).strip()



        add_memory(
            "name",
            name
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