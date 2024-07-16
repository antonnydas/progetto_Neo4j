import main_functions
from create_db import driver
from neo4j import GraphDatabase

uri = "neo4j+s://44abdaa3.databases.neo4j.io"
AUTH = ("neo4j", "k9W9xJ-oq7yb9SdzY8cuzo52snNHhuhLdqQAOGJA54Q")
driver = GraphDatabase.driver(uri, auth=AUTH)

# input di ricerca
person_name = input("Inserisci il nome del sospettato")  
date = input("Inserisci la data") 
time = input("Inserisci l'orario")    

# input di prova
# person_name = "Collin Lopez"         
# date = "2024-04-11"
# time = "10:15:19"

location = main_functions.get_person_location(driver, person_name, date, time)
if location:
    print(f"\nIl sospettato: {person_name}\nera collegato alle ore: {time}\nin data: {date}\nalla cella: {location['cell_name']}\ncon posizione: {location['cell_location']}")
else:
    print(f"Nessuna connessione trovata per {person_name} alla data e all'ora specificate")

