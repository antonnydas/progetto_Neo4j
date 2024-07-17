from neo4j import GraphDatabase
import os

def connect_to_db():
    uri = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")
    driver = GraphDatabase.driver(uri, auth=AUTH)
    return driver

def format_date(neo4j_date):
    return neo4j_date.strftime("%Y-%m-%d %H:%M")

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
