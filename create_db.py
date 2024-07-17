from datetime import datetime, timedelta
from neo4j import GraphDatabase
from faker import Faker
import random
import math

uri = "bolt://localhost:7687"
AUTH = ("neo4j", "password")
driver = GraphDatabase.driver(uri, auth=AUTH)

faker = Faker()
Faker.seed(0)

def reset_database(tx):
    tx.run("MATCH (n) DETACH DELETE n")

def generate_random_point(center_lat, center_lon, radius_km):
    with driver.session() as session:
        query = """
        WITH point({latitude: $center_lat, longitude: $center_lon}) AS center,
             $radius_km AS radius_km //Alias per rendere più semplice il richiamo degli elementi
        WITH center, radius_km / 111.0 AS radius_deg
        WITH center, radius_deg, rand() * 2 * pi() AS angle, rand() * radius_deg AS distance
        RETURN point({latitude: center.y + distance * cos(angle), longitude: center.x + distance * sin(angle)}) AS point
        """ #Creazione di un punto randomico nel raggio del radius_km tramite neo4j
        result = session.run(query, center_lat=center_lat, center_lon=center_lon, radius_km=radius_km)
        record = result.single()
        point = record["point"]
    
    latitude = point.y
    longitude = point.x
    
    return (latitude, longitude)

def create_data(tx, num_persons, num_cells, start_date = datetime(2024, 7, 18), end_date = datetime(2024, 8, 18) ):
    center_lat, center_lon = 45.4642, 9.19  # Coordinate di Milano come centro
    
    cells = []

    # Creazione delle celle prima della creazione dei nodi Persona e Ntel
    for _ in range(num_cells):
        while True:
            cell_name = f"cell{random.randint(1, 1000)}"
            if cell_name not in cells: #Check per evitare celle doppioni
                cell_location = generate_random_point(center_lat, center_lon, 20)
                tx.run("CREATE (c:Cella {nome: $nome, posizione: point({latitude: $lat, longitude: $lon})})",
                    nome=cell_name, lat=cell_location[0], lon=cell_location[1])
                cells.append((cell_name, cell_location))
                break
            else:
                continue

    # Creazione dei nodi Persona e NTel
    for _ in range(num_persons):
        person_name = faker.name()
        tx.run("CREATE (p:Persona {nome: $nome})", nome=person_name) #Grazie a faker genero il nome di una persona random e creo il nodo

        num_phones = random.choices([1, 2, 3], weights=[70, 25, 5])[0] #Ogni persona ha il 70% di possibilità di avere una sim, il 25% di averne 2 e il 5% di averne una
        phone_numbers = [faker.basic_phone_number() for _ in range(num_phones)] #Genero n numeri di telefono in base al numero di sim per persona
        for phone_number in phone_numbers:
            tx.run("MATCH (p:Persona {nome: $nome}) "
                   "CREATE (n:Sim {numeroTelefono: $numero})-[:POSSEDUTO_DA]->(p)", #Dopo averle matchate, assegno a ogni persona la propria sim e 
                   #annesso numero di telefono tramite la relazione "POSSEDUTO_DA"
                   nome=person_name, numero=phone_number)

        current_date = start_date 
        while current_date < end_date: #Check per non sforare l'intervallo di tempo
            cell_connections = []
            prima_sim_location = generate_random_point(center_lat, center_lon, 20) #Genero la posizione della prima sim per persona
            prima_cella_vicina = min(cells, key=lambda cell: math.dist(prima_sim_location, cell[1])) #Trovo la cella più vicina alla prima sim tramite la distanza euclidea
            prima_cella_vicina_nome = prima_cella_vicina[0] #Trovo il nome della detta cella più vicina

            for phone_number in phone_numbers: #Se c'è più di un numero di telefono
                if random.random() < 0.75: #75% di possibilità che le posizioni di 2 sim della stessa persona si sovrappongano
                    cell_connections.append((phone_number, prima_cella_vicina_nome, prima_sim_location))
                else: #25% di possibilità che le posizioni non si sovrappongano
                    sim_location = generate_random_point(center_lat, center_lon, 20) #Genero un'altra coordinata potenzialmente diversa da quella dell'altra sim
                    cella_vicina = min(cells, key=lambda cell: math.dist(sim_location, cell[1])) 
                    cella_vicina_nome = cella_vicina[0]
                    cell_connections.append((phone_number, cella_vicina_nome, sim_location))

            for phone_number, cell_name, phone_location in cell_connections:
                formatted_date = current_date.strftime("%Y-%m-%d %H:%M")  #Formatto la data in modo da renderla più leggibile
                tx.run("MATCH (n:Sim {numeroTelefono: $numero}), (c:Cella {nome: $nome}) "  # Matcho il numero di telefono interessato e la cella
                    "MERGE (n)-[r:CONNESSO_A]->(c) "  # Uso MERGE invece di CREATE per evitare di rendere ridondanti i grafi: se una relazione già esiste tra i due nodi, si terrà quella già presente.
                    "ON CREATE SET r.dates = [$data], r.posizione = [point({latitude: $lat, longitude: $lon})] " #Se dal MERGE risulta che la relazione non esiste
                    #anora, la creo e inizializzo le date e le posizioni come array, in caso ce ne siano di più.
                    "ON MATCH SET r.dates = r.dates + $data, r.posizione = r.posizione + point({latitude: $lat, longitude: $lon})", #Se invece risulta che la relazione
                    #già esiste, aggiorno semplicemente l'array
                    numero=phone_number, nome=cell_name, data=formatted_date, lat=phone_location[0], lon=phone_location[1])

            current_date += timedelta(hours=random.randint(12, 24)) #Aggiorno la data corrente per simulare un diverso momento dell'intervallo di tempo
            
with driver.session() as session: #Resetto il database e lo genero di nuovo
    session.execute_write(reset_database)
    session.execute_write(create_data, 15, 10)

driver.close()