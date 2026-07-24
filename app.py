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

/* FONT FIX */

.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp input,
.stApp textarea,
.stMarkdown,
.stButton button {

    font-family:"Berlin Sans FB", sans-serif !important;
    font-weight:normal !important;

}


.stApp{
    background:#ffffff;
}


/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:#0057B8;
}


section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] button{

    color:white !important;
    font-family:"Berlin Sans FB", sans-serif !important;
    font-weight:normal !important;

}


/* KEEP STREAMLIT SIDEBAR ARROWS */

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"]{

    font-family:initial !important;

}


[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg{

    display:block !important;

}


/* BUTTONS */

.stButton button{

    background:linear-gradient(
    135deg,
    #0057B8,
    #E31E24
    );

    color:white !important;

    border:none;

    border-radius:25px;

}


/* CHAT INPUT */

div[data-testid="stChatInput"]{

    border-radius:30px !important;

    background:white !important;

    box-shadow:
    0px 5px 20px rgba(0,0,0,0.15);

}


div[data-testid="stChatInput"] textarea{

    font-family:"Berlin Sans FB", sans-serif !important;

}


/* CHAT MESSAGE */

div[data-testid="stChatMessage"]{

    border-radius:20px;

    padding:15px;

}

/* RESTORE STREAMLIT SIDEBAR ARROW ICON */

[data-testid="stSidebarCollapseButton"] svg {
    display: inline-block !important;
    visibility: visible !important;
}


[data-testid="stSidebarCollapseButton"] span {
    font-size: 0 !important;
}


[data-testid="stSidebarCollapseButton"] span svg {
    width: 24px !important;
    height: 24px !important;
}


[data-testid="stSidebarCollapsedControl"] svg {
    display: inline-block !important;
    visibility: visible !important;
}


[data-testid="stSidebarCollapsedControl"] span {
    font-size: 0 !important;
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
font-family:'Berlin Sans FB',sans-serif;
">


<h1 style="
color:white;
font-weight:normal;
">
Where should we begin ?
</h1>


<p style="
font-weight:normal;
">
... D <3 is ready ...
</p>


</div>

""",
unsafe_allow_html=True)




# ================= SESSION =================


if "messages" not in st.session_state:

    st.session_state.messages=[]




# ================= SIDEBAR =================


with st.sidebar:


    st.markdown("""
<h1 style="
color:white;
font-weight:normal;
">
D <3 AI
</h1>


<p style="
font-weight:normal;
">
Your personal AI Assistant


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






            # TEXT TO SPEECH


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