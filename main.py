import main_functions
from create_db import driver
from neo4j import GraphDatabase


if __name__ == "__main__":

    uri = "neo4j+s://21d203cb.databases.neo4j.io"
    AUTH = ("neo4j", "nzbCTet_44-TGPjZEAvvSmjjORptwBCkT-fbtKiYAwU")
    driver = GraphDatabase.driver(uri, auth=AUTH)
    
    while True:
        main_functions.main_menu(driver)



