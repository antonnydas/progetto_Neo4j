import os
import time
from datetime import datetime, timedelta


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

def search_cell(driver):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ricerca per cella\n")
    time.sleep(2)
    pass


def find_nearby_cells(tx, latitude, longitude, start_datetime, end_datetime):
    query = """
        MATCH (:Sim)-[r:CONNESSO_A]->(c:Cella)
        WHERE point.distance(c.posizione, point({latitude: $latitude, longitude: $longitude})) < 5000
        AND datetime(r.dates[0]) >= datetime($start_datetime)
        AND datetime(r.dates[0]) <= datetime($end_datetime)
        MATCH (s:Sim)-[:POSSEDUTO_DA]->(p:Persona)
        RETURN p.nome AS persona, s.numeroTelefono AS numeroTelefono, c.nome AS cellaNome, c.posizione AS cellaPosizione
    """
    result = tx.run(query, latitude=latitude, longitude=longitude, start_datetime=start_datetime, end_datetime=end_datetime)
    return result.data()


def search_coordinate(driver):
    latitude = float(input("Inserisci la latitudine (es. 45.4642): "))
    longitude = float(input("Inserisci la longitudine (es. 9.19): "))
    start_datetime_str = input("Inserisci la data e l'orario di inizio (es. 2024-07-18 12:33): ")
    end_datetime_str = input("Inserisci la data e l'orario di fine (es. 2024-08-18 13:33): ")

    #conversione input in formato datetime e poi in formato ISO
    start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M").isoformat()
    end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M").isoformat()

    with driver.session() as session:
        records = session.read_transaction(find_nearby_cells, latitude, longitude, start_datetime, end_datetime)

        print("Le SIM collegate alle celle più vicine sono:")
        for record in records:
            persona = record['persona']
            numero_telefono = record['numeroTelefono']
            print(f"{persona} (con numero {numero_telefono})")

        print("Premi un tasto per tornare al menu principale")
        input()

def main_menu(driver):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Main Menu")
    print("1. Cerca persona\n"
          "2. Cerca per Cella\n"
          "3. Cerca per Coordinate\n"
          "4. Esci\n")

    choice = int(input("Scegli un'opzione: "))
    if choice == 1:
        cell_localization(driver)
        # input di prova
        # person_name = " Michael Anderson"
        # date = "2024-08-01 "
        # time = "12:00"
    elif choice == 2:
        search_cell(driver)
    elif choice == 3:
        search_coordinate(driver)
    elif choice == 4:
        print("Uscita dal programma\n")
        time.sleep(1)
        exit(0)
    else:
        print("Scelta non valida")
        return main_menu(driver)