import main_functions
from create_db import driver
from neo4j import GraphDatabase

uri = "neo4j+s://44abdaa3.databases.neo4j.io"
AUTH = ("neo4j", "k9W9xJ-oq7yb9SdzY8cuzo52snNHhuhLdqQAOGJA54Q")
driver = GraphDatabase.driver(uri, auth=AUTH)

# funzione di localizzazione cella in base a nome sospettato, data e ora.
main_functions.cell_localization(driver)

# input di prova

# person_name = "Collin Lopez" 
# date = "2024-04-11"
# time = "10:15:19"
