def check_wake_word(text):

    wake_words = [
        "hey assistant",
        "assistant",
        "hey ai"
    ]

    text = text.lower()

    for word in wake_words:
        if word in text:
            return True

    return False