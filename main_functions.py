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

def cell_localization(driver): 

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