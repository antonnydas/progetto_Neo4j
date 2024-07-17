import os
import time
from datetime import datetime, timedelta
import a_primo_requisito_query
import b_secondo_requisito_query
import c_terzo_requisito_query

def main_menu(driver):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Main Menu")
    print("1. Localizza sospettati\n"
          "2. Cerca sospettati per Cella\n"
          "3. Cerca sospettati per Coordinate\n"
          "4. Esci\n")

    choice = int(input("Scegli un'opzione: "))
    if choice == 1:

        name = input("Inserisci il nome del sospettato: ")

        start_date = input("Inserisci data iniziale (YYYY-MM-DD): ")
        start_time = input("Inserisci orario iniziale (HH:MM:SS): ")
        end_date = input("Inserisci data finale (YYYY-MM-DD): ")
        end_time = input("Inserisci orario finale (HH:MM:SS): ")

        start_date_time = f"{start_date}T{start_time}"
        end_date_time = f"{end_date}T{end_time}"

        a_primo_requisito_query.return_results_one(name, start_date_time, end_date_time)

        input("Premere un tasto per continuare..")

        # input di prova
        # person_name = " Michael Anderson"
        # date = "2024-08-01 "
        # time = "12:00"

    elif choice == 2:

        cell_name = input("Inserisci il nome della cella: ")

        start_date = input("Inserisci data iniziale (YYYY-MM-DD): ")
        start_time = input("Inserisci orario iniziale (HH:MM:SS): ")
        end_date = input("Inserisci data finale (YYYY-MM-DD): ")
        end_time = input("Inserisci orario finale (HH:MM:SS): ")

        start_date_time = f"{start_date}T{start_time}"
        end_date_time = f"{end_date}T{end_time}"

        b_secondo_requisito_query.return_results_two(cell_name, start_date_time, end_date_time )

        input("Premere un tasto per continuare..")
        
        # input di prova
        # "cell958"
        # "2024-07-18"
        # "2024-08-18"

    elif choice == 3:

        latitude = input("Inserisci la latitudine: ")
        longitude = input("Inserisci longitudine: ")
        radius = input("Inserisci il raggio: ")

        start_date = input("Inserisci data iniziale (YYYY-MM-DD): ")
        start_time = input("Inserisci orario iniziale (HH:MM:SS): ")
        end_date = input("Inserisci data finale (YYYY-MM-DD): ")
        end_time = input("Inserisci orario finale (HH:MM:SS): ")

        start_date_time = f"{start_date}T{start_time}"
        end_date_time = f"{end_date}T{end_time}"
        
        c_terzo_requisito_query.return_results_three(latitude, longitude, radius, start_date_time, end_date_time)
        
        input("Premere un tasto per continuare..")

        # input di prova
        # latitude = 45.95969977582438
        # longitude = 9.365010069276185
        # radius = 40
        # start_date = "2024-07-1T00:00:00"
        # end_date = "2024-07-19T00:00:10"

    elif choice == 4:
        print("Uscita dal programma\n")
        time.sleep(1)
        exit(0)
    else:
        print("Scelta non valida")
        return main_menu(driver)