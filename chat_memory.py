import json
import os


FILE = "chat_history.json"


def get_history():

    if not os.path.exists(FILE):
        return []

    try:

        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:

        return []



def add_message(role, content):

    history = get_history()

    history.append(
        {
            "role": role,
            "content": content
        }
    )

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False
        )