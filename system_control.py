import os

def open_application(command):
    command = command.lower()

    if "calculator" in command:
        os.system("calc")
        return "Opening calculator"

    elif "notepad" in command:
        os.system("notepad")
        return "Opening notepad"

    else:
        return None
