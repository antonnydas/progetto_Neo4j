from neo4j import GraphDatabase

URI = "neo4j+s://fc620fee.databases.neo4j.io"
AUTH = ("neo4j", "NbxsUXZ91m0V1axpg953YHuLuZqJu3e9L25zG7auz2A")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("OK")