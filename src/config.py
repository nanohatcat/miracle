import configparser
import os

DEFAULT = {
    "scroll_speed": "0.15",
    "cache": "true",
    "lrc": "true",
    "colors": "true",
    "ipc": "false"
}

def load_config():
    path = os.path.expanduser("~/.config/miracle/config.ini")

    cfg = configparser.ConfigParser()
    cfg["main"] = DEFAULT

    if os.path.exists(path):
        cfg.read(path)

    return cfg["main"]
