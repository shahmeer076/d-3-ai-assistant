from speech_to_text import listen
from llm import ask_ai
from text_to_speech import speak
from wake_word import check_wake_word
from commands import run_command
from memory import save_memory, get_memory


while True:

    user_input = listen()

    if user_input.lower() == "exit":
        speak("Goodbye")
        break


    if not check_wake_word(user_input):
        continue


    speak("Yes, how can I help you?")

    user_input = listen()


    if user_input.lower() == "exit":
        speak("Goodbye")
        break


    text = user_input.lower()


    if "my name is" in text:

        name = text.replace("my name is", "").strip()

        save_memory("name", name)

        response = f"Okay, I will remember your name {name}"

        print("AI:", response)
        speak(response)

        continue


    elif "what is my name" in text or "who am i" in text or "what's my name" in text:

        name = get_memory("name")

        if name == "I don't remember":
            response = "I don't know your name yet"
        else:
            response = f"Your name is {name}"

        print("AI:", response)
        speak(response)

        continue


    command = run_command(user_input)


    if command:
        print("AI:", command)
        speak(command)
        continue


    response = ask_ai(user_input)

    print("AI:", response)

    speak(response)