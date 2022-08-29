from collections import OrderedDict

import commands

from presentation import (
    Option,
    get_new_client_data,
    get_client_id,
    clear_screen,
    print_options,
    get_option_choice,
    get_file_name,
    get_update_client_data,
    # get_email
)


def loop():
    options = OrderedDict(
        {
            "A": Option("Creaza o fisa client", commands.AddClientCommand(), prep_call=get_new_client_data),
            "B": Option("Afiseaza o fisa client dupa nr de inregistrare", commands.GetClientCommand(), prep_call=get_client_id),
            "C": Option("Afiseaza fisele clienti in ordinea intrarii", commands.ListClientsCommand()),
            "D": Option("Afiseaza fisele clienti in ordine alfabetica", commands.ListClientsCommand(order_by="client_name")),
            "E": Option("Editeaza o fisa client", commands.EditClientCommand(), prep_call=get_update_client_data),
            "F": Option("Creaza un cod QR", commands.CreateQRCommand(), prep_call=get_client_id),
            "G": Option("Export to Excel", commands.ExportToExcelCommand(), prep_call=get_file_name),
            # "M": Option("Email the bookmarks", commands.EmailCommand(), prep_call=get_email),
            "Q": Option("Iesi din program", commands.QuitCommand())
        }
    )

    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    clear_screen()
    new_func(chosen_option)
    _ = input("Press ENTER to return to menu")

def new_func(chosen_option):
    chosen_option.choose()

if __name__ == "__main__":
    print("Fise Clienti")
    commands.CreateClientsTableCommand().execute()
    
    while True:
        loop()