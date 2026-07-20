import speech_recognition as sr

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak...")
        
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text

    except:
        print("Sorry, I didn't understand")
        return "" 