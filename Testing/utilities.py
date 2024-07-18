from neo4j import GraphDatabase
import os
from datetime import datetime
import platform

def connect_to_db():
    uri = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")
    driver = GraphDatabase.driver(uri, auth=AUTH)
    return driver

def format_date(date):
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    
    return date.strftime("%Y-%m-%d %H:%M")



def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
