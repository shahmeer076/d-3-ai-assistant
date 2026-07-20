import pyttsx3


def speak(text):

    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")

    for voice in voices:
        name = voice.name.lower()
        if "female" in name or "zira" in name or "samantha" in name:
            engine.setProperty("voice", voice.id)
            break

    text = str(text)

    sentences = text.split(".")

    for sentence in sentences:
        if sentence.strip():
            engine.say(sentence.strip())

    engine.runAndWait()

    engine.stop()