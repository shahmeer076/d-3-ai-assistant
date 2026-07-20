import datetime
import webbrowser



def run_command(text):


    text = text.lower()



    # Time command

    if "time" in text:


        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )


        return f"The current time is {current_time}"





    # Open YouTube

    elif "open youtube" in text or "youtube kholo" in text:


        webbrowser.open(
            "https://www.youtube.com"
        )


        return "Opening YouTube"






    # Open Google

    elif "open google" in text or "google kholo" in text:


        webbrowser.open(
            "https://www.google.com"
        )


        return "Opening Google"







    # Google search

    elif "search google" in text:


        query = text.replace(
            "search google",
            ""
        ).strip()



        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )


        return f"Searching Google for {query}"







    # YouTube search

    elif "search youtube" in text:


        query = text.replace(
            "search youtube",
            ""
        ).strip()



        webbrowser.open(
            f"https://www.youtube.com/results?search_query={query}"
        )


        return f"Searching YouTube for {query}"






    return None