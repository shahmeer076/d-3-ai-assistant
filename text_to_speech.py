from gtts import gTTS
import tempfile
import os


def speak(text):

    text = str(text)

    try:

        tts = gTTS(
            text=text,
            lang="en"
        )


        file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )


        tts.save(
            file.name
        )


        return file.name


    except Exception as e:

        print("TTS Error:", e)

        return None
        