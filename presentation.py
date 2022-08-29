import os

from typing import Callable, Dict, Union

import commands


class Option:
    def __init__(self, name: str, command: commands.Command, prep_call: Callable = None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def _handle_message(self, message: Union[str, list]):
        if isinstance(message, list):
            for entry in message:
                print(entry)
        else:
            print(message)

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        self._handle_message(message)

    def __str__(self):
        return self.name


def print_options(options: Dict[str, Option]):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice: str, options: Dict[str, Option]) -> bool:
    return choice in options or choice.upper() in options


def get_option_choice(options: Dict[str, Option]) -> Option:
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice!")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label: str, required: bool = True) -> Union[str, None]:
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


def get_new_client_data() -> dict:
    return {
        "client_name": get_user_input("Client_name"),
        "proiect": get_user_input("proiect"),
        "informatii": get_user_input("informatii"),
        "adresa": get_user_input("adresa", required=False),
    }


def get_update_client_data() -> dict:
    client_id = int(get_user_input("Tasteaza nr de inregistrare a clientului"))
    field = get_user_input("Alege ce vrei sa editezi (client_name, proiect, status, adresa)")
    new_value = get_user_input(f"Enter a new value for {field}")
    return {
        "id": client_id,
        "update": {
            field: new_value
        }
    }


def get_file_name() -> str:
    file_name = get_user_input("Cum vrei sa salvezi fisierul?: ")
    return file_name


def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)


def get_client_id():
    return int(get_user_input("Introdu un nr de inregistrare"))




# def get_email():
#     recipient = get_user_input("Enter an email")
    
#     return {
#         "recipient": recipient
#     }