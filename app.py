import streamlit as st
from llm import ask_ai
import streamlit.components.v1 as components


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

st.markdown("### 🎤 Voice Input")


voice_html = """
<script>
function startListening(){

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = function(event){

        const text = event.results[0][0].transcript;

        window.parent.postMessage(
            {
                type:"streamlit:setComponentValue",
                value:text
            },
            "*"
        );
    }

    recognition.start();
}

</script>

<button onclick="startListening()">
🎤 Speak
</button>
"""


components.html(
    voice_html,
    height=100
)

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

st.components.v1.html(
f"""
<script>

let speech = new SpeechSynthesisUtterance(
"{response}"
);

speech.lang="en-US";

window.speechSynthesis.speak(speech);

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