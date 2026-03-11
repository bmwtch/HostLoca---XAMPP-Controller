# main.py
import tkinter as tk
from gui.app_gui import ControlPanelApp
import json
import os

# Config in AppData\Roaming\HostLoca
CONFIG_PATH = os.path.join(os.getenv("APPDATA"), "HostLoca", "settings.json")

def load_settings():
    defaults = {
        "xampp_path": "",
        "htdocs_path": "",
        "sql_folder": "",
        "db_user": "root",
        "db_pass": ""
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = f.read().strip()
                if not data:
                    return defaults
                return json.loads(data)
        except Exception:
            return defaults
    return defaults

def save_settings(settings):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings, f, indent=4)

def main():
    settings = load_settings()

    root = tk.Tk()
    root.title("HostLoca - XAMPP Controller || © Brahman WebTech - www.bmwtech.in")
    root.geometry("800x550")
    root.resizable(False, False)
    root.option_add("*Font", ("Segoe UI", 10))
    ControlPanelApp(root, settings, save_settings)

    root.mainloop()

if __name__ == "__main__":
    main()
