import os
from neo4j import GraphDatabase
from datetime import datetime
import pandas as pd
from tabulate import tabulate
from collections import defaultdict
from utilities import *

driver = connect_to_db()

def primo_requisito_query(driver, person_name, start_date, end_date):
    query = """
    MATCH (c:Cella)<-[r:CONNESSO_A]-(s:Sim)-[:POSSEDUTO_DA]->(p:Persona {nome: $person_name}) 
    WITH c, s, r, 
         [date IN r.dates WHERE datetime($start_date) <= datetime(date) <= datetime($end_date)] AS filtered_dates //Filtra tutte le date che risultano all'interno del range
    WHERE size(filtered_dates) > 0 //Check per assicurarsi che si prendano solo le relazioni che hanno effettivamente una data all'interno del range definito
    RETURN c, s, filtered_dates AS dates //Vengono date in output le celle, le sim e le date e orari di connessione delle sim a queste celle
    """
    with driver.session() as session:
        result = session.run(query, person_name=person_name, start_date=start_date, end_date=end_date)
        return [(record["c"], record["s"], record["dates"]) for record in result]

def create_dataframe(results):
    datas = defaultdict(list)
    for cell, sim, dates in results:
        for date in dates:
            datas[sim["numeroTelefono"]].append({ 
                "Data": format_date(date),
                "Numero": sim["numeroTelefono"],
                "Cella": cell["nome"],
            }) #Ottengo un dizionario che ha come key i numeri di telefono della persona, e come valore una lista di dizionari per ogni registrazione
            #del numero di telefono associato alla sim.
    
    all_data = []
    for _, entries in datas.items():
        sorted_entries = sorted(entries, key=lambda x: x["Data"]) 
        all_data.extend(sorted_entries) #Sorto in base alla data tutti i valori del precedente dizionario e li unisco in un'unica lista di dizionarii ordinati
    
    df = pd.DataFrame(all_data) #Converto il tutto in un dataframe
    return df

def return_results_one(person_name, start_date, end_date):
    results = primo_requisito_query(driver, person_name, start_date, end_date)
    
    df = create_dataframe(results)
    
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False)) #Uso di Tabulate per questioni estetiche
    
    tabulati_dir = os.path.join(os.getcwd(), "tabulati")
    create_directory(tabulati_dir)
    
    tabulati_persona_date_dir = os.path.join(tabulati_dir, "tabulati_persona_date")
    create_directory(tabulati_persona_date_dir)
    
    start_date= start_date.replace(':', '-')
    end_date = end_date.replace(':', '-')
    csv_filename = f"{person_name}_{start_date}_{end_date}_connections.csv"
    csv_path = os.path.join(tabulati_persona_date_dir, csv_filename)

    df.to_csv(csv_path, index=False) #Dopo aver creato la path, salvo il dataframe come CSV
    print(f"\nFile CSV '{csv_filename}' creato nella directory: {tabulati_persona_date_dir}")

        
    driver.close()

if __name__ == '__main__':

    return_results_one("Norma Fisher", "2024-07-18", "2024-08-18")
