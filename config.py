from json import load, dump


def load_data(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return load(f)
    except FileNotFoundError:
        return None


def save_data(data, file) -> None:
    with open(file, "w+", encoding='utf-8') as f:
        dump(data, f, indent=4)
        f.truncate()
        return

default_configuration = {
        "name": None,
        "greetings": {
            "enabled": True,
            "channel": None
        },
        "reaction-roles": {
            "enabled": True
        },
        "chat-filter": {
            "enabled": True,
            "log-channel": None,
            "use-default-list": True,
            "custom-words": [],
            "whitelisted-channels": [],
            "whitelisted-members": []
        },
        "mute": {
            "enabled": True,
            "muted-members": []
        }
    }

config = load_data("./data/serverconfig.json")
greetings = load_data("./data/greetings.json")
