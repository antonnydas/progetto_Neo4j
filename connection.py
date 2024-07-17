from neo4j import GraphDatabase

def connect_to_db():
    AUTH = ("neo4j", "k9W9xJ-oq7yb9SdzY8cuzo52snNHhuhLdqQAOGJA54Q")
    URI = "neo4j+s://44abdaa3.databases.neo4j.io"
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("OK")

        with driver.session() as sessione:
            sessione.run("CREATE(n:Cella{name:'OOOOO',title:'prova'})")