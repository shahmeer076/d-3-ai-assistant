import customtkinter as ctk
import threading

from speech_to_text import listen
from text_to_speech import speak
from commands import run_command
from llm import ask_ai
from memory import save_memory, get_memory


# ================= THEME =================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


app = ctk.CTk()

app.title("Meeru's Assistant")
app.geometry("1200x750")
app.configure(fg_color="#F7F9FC")



# ================= VARIABLES =================

messages = []



# ================= FUNCTIONS =================


def add_message(sender, message):

    messages.append((sender, message))

    create_chat_bubble(sender, message)



def create_chat_bubble(sender, message):

    if sender == "You":

        bubble = ctk.CTkFrame(
            chat_area,
            fg_color="#2563EB",
            corner_radius=20
        )

        label = ctk.CTkLabel(
            bubble,
            text=message,
            text_color="white",
            font=("Berlin Sans FB",16),
            wraplength=500,
            justify="left"
        )

        label.pack(
            padx=15,
            pady=10
        )

        bubble.pack(
            anchor="e",
            pady=8,
            padx=20
        )


    else:

        bubble = ctk.CTkFrame(
            chat_area,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=1,
            border_color="#D1D5DB"
        )

        label = ctk.CTkLabel(
            bubble,
            text=message,
            text_color="#111827",
            font=("Berlin Sans FB",16),
            wraplength=500,
            justify="left"
        )

        label.pack(
            padx=15,
            pady=10
        )


        bubble.pack(
            anchor="w",
            pady=8,
            padx=20
        )



def clear_chat():

    for widget in chat_area.winfo_children():

        widget.destroy()

    messages.clear()



def get_response(user_input):

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


        return f"I will remember your name {name}"



    elif "what is my name" in text or "who am i" in text:

        name = get_memory("name")

        return f"Your name is {name}"



    command = run_command(user_input)


    if command:

        return command



    return ask_ai(user_input)




def send_message():

    user = message_entry.get().strip()


    if user == "":

        return


    message_entry.delete(
        0,
        "end"
    )


    add_message(
        "You",
        user
    )



    def reply():

        try:

            response = get_response(user)


            add_message(
                "AI",
                response
            )


            speak(response)


        except Exception as e:


            add_message(
                "AI",
                str(e)
            )


    threading.Thread(
        target=reply,
        daemon=True
    ).start()




def voice_chat():


    def run():

        try:

            user = listen()


            if user:


                add_message(
                    "You",
                    user
                )


                response = get_response(user)


                add_message(
                    "AI",
                    response
                )


                speak(response)


        except Exception as e:

            add_message(
                "AI",
                str(e)
            )



    threading.Thread(
        target=run,
        daemon=True
    ).start()



def new_chat():

    clear_chat()

    add_message(
        "AI",
        "New chat started. How can I help you?"
    )



def show_history():

    clear_chat()

    for sender,msg in messages:

        create_chat_bubble(
            sender,
            msg
        )



# ================= SIDEBAR =================


sidebar = ctk.CTkFrame(
    app,
    width=250,
    corner_radius=0,
    fg_color="#111827"
)

sidebar.pack(
    side="left",
    fill="y"
)



logo = ctk.CTkLabel(
    sidebar,
    text="D <3",
    font=("Berlin Sans FB",40,"bold"),
    text_color="white"
)

logo.pack(
    pady=30
)



new_chat_btn = ctk.CTkButton(
    sidebar,
    text="+ New Chat",
    height=45,
    corner_radius=15,
    fg_color="#2563EB",
    command=new_chat
)

new_chat_btn.pack(
    padx=20,
    pady=10,
    fill="x"
)



history_btn = ctk.CTkButton(
    sidebar,
    text="🕘 History",
    height=45,
    corner_radius=15,
    fg_color="#374151",
    command=show_history
)

history_btn.pack(
    padx=20,
    pady=10,
    fill="x"
)



voice_btn = ctk.CTkButton(
    sidebar,
    text="🎤 Voice Chat",
    height=45,
    corner_radius=15,
    fg_color="#10B981",
    command=voice_chat
)

voice_btn.pack(
    padx=20,
    pady=10,
    fill="x"
)



clear_btn = ctk.CTkButton(
    sidebar,
    text="🗑 Clear Chat",
    height=45,
    corner_radius=15,
    fg_color="#EF4444",
    command=clear_chat
)

clear_btn.pack(
    padx=20,
    pady=10,
    fill="x"
)# ================= MAIN AREA =================


main_area = ctk.CTkFrame(
    app,
    fg_color="#F7F9FC",
    corner_radius=0
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)



# ================= HEADER =================


header = ctk.CTkLabel(
    main_area,
    text="D <3",
    font=("Berlin Sans FB",40,"bold"),
    text_color="#1E3A8A"
)

header.pack(
    pady=25
)



# ================= CHAT AREA =================


chat_container = ctk.CTkFrame(
    main_area,
    fg_color="#FFFFFF",
    corner_radius=25,
    border_width=1,
    border_color="#D1D5DB"
)

chat_container.pack(
    padx=25,
    pady=10,
    fill="both",
    expand=True
)



chat_area = ctk.CTkScrollableFrame(
    chat_container,
    fg_color="white",
    corner_radius=20
)

chat_area.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)



# ================= INPUT AREA =================


input_frame = ctk.CTkFrame(
    main_area,
    fg_color="#EAF2FF",
    corner_radius=25
)

input_frame.pack(
    padx=25,
    pady=20,
    fill="x"
)



message_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your message...",
    height=55,
    font=("Berlin Sans FB",16),
    corner_radius=25,
    fg_color="white",
    text_color="black"
)


message_entry.pack(
    side="left",
    padx=15,
    pady=10,
    fill="x",
    expand=True
)



send_btn = ctk.CTkButton(
    input_frame,
    text="➤",
    width=60,
    height=50,
    corner_radius=20,
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    font=("Arial",20),
    command=send_message
)

send_btn.pack(
    side="right",
    padx=5
)



mic_btn = ctk.CTkButton(
    input_frame,
    text="🎤",
    width=60,
    height=50,
    corner_radius=20,
    fg_color="#10B981",
    hover_color="#059669",
    font=("Arial",20),
    command=voice_chat
)


mic_btn.pack(
    side="right",
    padx=5
)



# ================= WELCOME MESSAGE =================


add_message(
    "AI",
    "Hello Shahmeer 👋\nHow can I help you today?"
)



# ================= RUN =================


app.mainloop()