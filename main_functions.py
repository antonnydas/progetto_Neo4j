import os
import time


# funzione di localizzazione cella per nome sospetto, data e ora.
def get_person_location (driver, person_name, date, time):
    def find_cell_by_person_and_time(tx):
        query = """
        MATCH (p:Persona {nome: $person_name})<-[:POSSEDUTO_DA]-(n:N_Tel)-[:CONNESSO_A{data: date($date), orario: $time}]->(c:Cella)
        RETURN c.nome AS cell_name, c.posizione AS cell_location
        """
        result = tx.run(query, person_name=person_name, date=date, time=time)
        return result.single()

    with driver.session() as session:
        record = session.read_transaction(find_cell_by_person_and_time)
        if record:
            return {
                "cell_name": record["cell_name"],
                "cell_location": record["cell_location"]
            }
        else:
            return None

 # funzione di localizzazione cella in base a nome sospettato, data e ora.
def cell_localization(driver):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ricerca per persona\n")

    # input di ricerca
    person_name = input("Inserisci il nome del sospettato: ") 
    date = input("Inserisci la data: ") 
    time = input("Inserisci l'orario: ") 
    
    # utilizzo funzione di ricerca
    location = get_person_location(driver, person_name, date, time)
    if location:
        print(f"\nIl sospettato: {person_name}\nera collegato alle ore: {time}\nin data: {date}\nalla cella: {location['cell_name']}\ncon posizione: {location['cell_location']}\n")
    else:
        print(f"\nNessuna connessione trovata per {person_name} alla data e all'ora specificate\n")

    print("Premi un tasto per tornare al menu principale")
    input()

def search_cell():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ricerca per cella\n")
    time.sleep(2)
    pass


def search_coordinate():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ricerca per coordinate\n")
    time.sleep(2)
    pass


def main_menu(driver):
    print("Main Menu")
    print("1. Cerca persona\n"
          "2. Cerca per Cella\n"
          "3. Cerca per Coordinate\n"
          "4. Esci\n")

    choice = int(input("Scegli un'opzione: "))
    if choice == 1:
        cell_localization(driver)
        # input di prova
        # person_name = "Collin Lopez"
        # date = "2024-04-11"
        # time = "10:15:19"
    elif choice == 2:
        search_cell()
    elif choice == 3:
        search_coordinate()
    elif choice == 4:
        print("Uscita dal programma\n")
        time.sleep(1)
        exit(0)
    else:
        print("Scelta non valida")
        return main_menu(driver)