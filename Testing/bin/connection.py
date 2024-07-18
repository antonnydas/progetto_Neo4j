from neo4j import GraphDatabase

def connect_to_db():
    URI = "neo4j+s://21d203cb.databases.neo4j.io"
    AUTH = ("neo4j", "nzbCTet_44-TGPjZEAvvSmjjORptwBCkT-fbtKiYAwU")
   
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("OK")
