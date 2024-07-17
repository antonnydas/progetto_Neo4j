import os
from neo4j import GraphDatabase
from datetime import datetime
import pandas as pd
from tabulate import tabulate
from collections import defaultdict

uri = "bolt://localhost:7687"
AUTH = ("neo4j", "password")
driver = GraphDatabase.driver(uri, auth=AUTH)

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

def format_date(neo4j_date):
    return neo4j_date.strftime("%Y-%m-%d %H:%M")

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

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def return_results(cell_name, start_date, end_date):
    results = secondo_requisito_query(driver, cell_name, start_date, end_date)
    
    df = create_dataframe(results)
    
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
    
    tabulati_dir = os.path.join(os.getcwd(), "tabulati")
    create_directory(tabulati_dir)
    
    tabulati_cella_date_dir = os.path.join(tabulati_dir, "tabulati_cella_date")
    create_directory(tabulati_cella_date_dir)
    
    csv_filename = f"{cell_name}_{start_date}_{end_date}_people.csv"
    csv_path = os.path.join(tabulati_cella_date_dir, csv_filename)
    
    df.to_csv(csv_path, index=False)
    print(f"\nFile CSV '{csv_filename}' creato nella directory: {tabulati_cella_date_dir}")

    driver.close()

return_results("cell440", "2024-07-19T19:00:00", "2024-07-21T19:00:01")