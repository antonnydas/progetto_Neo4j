import main_functions
from create_db import driver
from neo4j import GraphDatabase

if __name__ == "__main__":

    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri)
    while True:
        main_functions.main_menu(driver)



