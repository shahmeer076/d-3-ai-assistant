import datetime
import webbrowser


def run_command(text):

    text = text.lower()

    print("Command received:", text)

    if "time" in text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"


    elif "youtube" in text or "you tube" in text:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"


    elif "google" in text:
        webbrowser.open("https://www.google.com")
        return "Opening Google"


    return None