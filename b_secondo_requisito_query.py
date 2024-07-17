import os
from neo4j import GraphDatabase
from datetime import datetime
import pandas as pd
from tabulate import tabulate
from collections import defaultdict
from utilities import *

driver = connect_to_db()

def secondo_requisito_query(driver, cell_name, start_date, end_date):
    query = """
    MATCH (c:Cella {nome: $cell_name})<-[r:CONNESSO_A]-(s:Sim)-[:POSSEDUTO_DA]->(p:Persona)
    WITH c, s, r, p,
         [date IN r.dates WHERE datetime($start_date) <= datetime(date) <= datetime($end_date)] AS filtered_dates
    WHERE size(filtered_dates) > 0
    RETURN c, s, p, filtered_dates AS dates 
    """
    #Questa query è quasi identica rispetto a quella per il primo requisito, cambia praticamente solo il fatto che stabolta l'utente definisce la cella, e la persona resta generica
    with driver.session() as session:
        result = session.run(query, cell_name=cell_name, start_date=start_date, end_date=end_date)
        return [(record["c"], record["s"], record["p"], record["dates"]) for record in result]

def create_dataframe(results):
    datas = defaultdict(list)
    for cell, sim, person, dates in results:
        for date in dates:
            datas[person["nome"]].append({
                "Data": format_date(date),
                "Numero": sim["numeroTelefono"],
                "Cella": cell["nome"],
                "Persona": person["nome"],
            })
    
    all_data = []
    for _, entries in datas.items():
        sorted_entries = sorted(entries, key=lambda x: x["Data"])
        all_data.extend(sorted_entries)
    
    df = pd.DataFrame(all_data)
    return df

def return_results_two(cell_name, start_date, end_date):
    results = secondo_requisito_query(driver, cell_name, start_date, end_date)
    
    df = create_dataframe(results)
    
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    
    tabulati_dir = os.path.join(os.getcwd(), "tabulati")
    create_directory(tabulati_dir)
    
    tabulati_cella_date_dir = os.path.join(tabulati_dir, "tabulati_cella_date")
    create_directory(tabulati_cella_date_dir)

    start_date = start_date.replace(':', '-')
    end_date = end_date.replace(':', '-')
    csv_filename = f"{cell_name}_{start_date}_{end_date}_people.csv"
    csv_path = os.path.join(tabulati_cella_date_dir, csv_filename)
    
    df.to_csv(csv_path, index=False)
    print(f"\nFile CSV '{csv_filename}' creato nella directory: {tabulati_cella_date_dir}")

    driver.close()

if __name__ == '__main__':

    return_results_two("cell958", "2024-07-18", "2024-08-18")