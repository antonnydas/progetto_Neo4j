import main_functions
from create_db import driver
from neo4j import GraphDatabase
from utilities import connect_to_db

if __name__ == "__main__":

    driver = connect_to_db()
    
    while True:
        main_functions.main_menu(driver)



