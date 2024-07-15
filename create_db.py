from datetime import datetime
from neo4j import GraphDatabase
from faker import Faker
import random
import json
import math

"""

modulo per la creazione del database neo4j
ATTENZIONE: eseguendo il seguente modulo, il database al quale si è connessi verrà sovrascritto e i dati precedenti
verranno eliminati 

"""
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri)

faker = Faker()
Faker.seed(0)

def reset_database(tx):
    tx.run("MATCH (n) DETACH DELETE n")

#funzione per generare un punto geojson entro un raggio di 20 km
def generate_geojson_point(center_lat, center_lon, radius_km):
    radius_deg = radius_km / 111  # Convert km to degrees (approx)
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius_deg)
    lat = center_lat + distance * math.cos(angle)
    lon = center_lon + distance * math.sin(angle)
    return json.dumps({"type": "Point", "coordinates": [lon, lat]})


def create_data(tx, num_persons):
    center_lat, center_lon = 45.4642, 9.19  # Coordinate di Milano come centro
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 7, 1)
    for _ in range(num_persons):
        # Creazione dei nodi Persona
        person_name = faker.name()
        tx.run("CREATE (p:Persona {nome: $nome})", nome=person_name)

        phone_number = faker.basic_phone_number()
        phone_location = generate_geojson_point(center_lat, center_lon, 20)
        tx.run("MATCH (p:Persona {nome: $nome}) "
               "CREATE (n:N_Tel {numero: $numero, posizione: $posizione})-[:POSSEDUTO_DA]->(p)",
               nome=person_name, numero=phone_number, posizione=phone_location)

        cell_name = f"Cella_{random.randint(1, 1000)}"
        cell_location = generate_geojson_point(center_lat, center_lon, 20)
        tx.run("CREATE (c:Cella {nome: $nome, posizione: $posizione})", nome=cell_name, posizione=cell_location)

        date = faker.date_between_dates(date_start=start_date, date_end=end_date)
        time = faker.time()
        tx.run("MATCH (n:N_Tel {numero: $numero}), (c:Cella {nome: $nome}) "
               "CREATE (n)-[:CONNESSO_A {data: $data, orario: $orario}]->(c)",
               numero=phone_number, nome=cell_name, data=date, orario=time)

with driver.session() as session:
    #ATTENZIONE: il database verrà resettato
    session.write_transaction(reset_database)  # Reset del database
    session.write_transaction(create_data, 10)  # Sostituisci 10 con il numero di persone desiderate

driver.close()
