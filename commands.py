import datetime


def run_command(text):

    text = text.lower()


    print("Command received:", text)


    if "time" in text:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}"


    elif "youtube" in text or "you tube" in text:

        return "Opening YouTube: https://www.youtube.com"


    elif "google" in text:

        return "Opening Google: https://www.google.com"


    return None