import main_functions
from create_db import driver
from neo4j import GraphDatabase

if __name__ == "__main__":

    uri = "neo4j+s://44abdaa3.databases.neo4j.io"
    AUTH = ("neo4j", "k9W9xJ-oq7yb9SdzY8cuzo52snNHhuhLdqQAOGJA54Q")
    driver = GraphDatabase.driver(uri, auth=AUTH)
    while True:
        main_functions.main_menu(driver)



