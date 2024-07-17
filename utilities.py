from neo4j import GraphDatabase
import os
from datetime import datetime

def connect_to_db():
    uri = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")
    driver = GraphDatabase.driver(uri, auth=AUTH)
    return driver

def format_date(date_str):
    neo4j_date = datetime.fromisoformat(date_str)
    return neo4j_date.strftime("%Y-%m-%d %H:%M")


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
