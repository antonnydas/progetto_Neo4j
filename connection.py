from neo4j import GraphDatabase
import os


def connect_to_db():
    AUTH = ("neo4j", "k9W9xJ-oq7yb9SdzY8cuzo52snNHhuhLdqQAOGJA54Q")
    URI = "neo4j+s://44abdaa3.databases.neo4j.io"
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("OK")

        with driver.session() as sessione:
            sessione.run("CREATE(n:Cella{name:'OOOOO',title:'prova'})")


def search_person():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ricerca per persona\n")
    pass

def search_cell():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ricerca per cella\n")
    pass

def search_coordinate():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ricerca per coordinate\n")
    pass


def main_menu():
    print("Main Menu")
    print("1. Cerca persona\n"
          "2. Cerca per Cella\n"
          "3. Cerca per Coordinate\n")

    choice = int(input("Scegli un'opzione: "))
    if choice == 1:
        search_person()
    elif choice == 2:
        search_cell()
    elif choice == 3:
        search_coordinate()
    else:
        print("Scelta non valida")
        return main_menu()


if __name__ == '__main__':

    driver = connect_to_db()

    while True:
        main_menu()