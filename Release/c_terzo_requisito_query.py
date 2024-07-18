import os
from neo4j import GraphDatabase
from datetime import datetime
import pandas as pd
from tabulate import tabulate
from collections import defaultdict
from utilities import *

driver = connect_to_db()

def terzo_requisito_query(driver, latitude, longitude, radius, start_datetime, end_datetime):
    latitude = float(latitude)
    longitude = float(longitude)
    radius = float(radius)
    query = """
    MATCH (s:Sim)-[r:CONNESSO_A]->(c:Cella)
    WHERE point.distance(point({latitude: $latitude, longitude: $longitude}), c.posizione) <= $radius*1000
    WITH s, r, c,
    [date IN r.dates WHERE datetime($start_datetime) <= datetime(date) <= datetime($end_datetime)] AS filtered_dates
    WHERE size(filtered_dates) > 0
    MATCH (s)-[:POSSEDUTO_DA]->(p:Persona)
    RETURN c, s, p, filtered_dates AS dates
    """

    start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")

    with driver.session() as session:
        result = session.run(query, latitude=latitude, longitude=longitude, radius=radius, start_datetime=start_datetime, end_datetime=end_datetime)
        return [(record["c"], record["s"], record["p"], record["dates"]) for record in result]

def create_dataframe(results):
    datas = defaultdict(list)
    for cell, sim, person, dates in results:
        for date in dates:
            datas[person["nome"]].append({
            "Data": format_date(date),
            "Numero": sim["numeroTelefono"],
            "Cella": cell["nome"],
            "Posizione": f"({cell['posizione'].y}, {cell['posizione'].x})",
            "Persona": person["nome"],
            })

    all_data = []
    for _, entries in datas.items():
        sorted_entries = sorted(entries, key=lambda x: x["Data"])
        all_data.extend(sorted_entries)

    df = pd.DataFrame(all_data)
    return df

def return_results_three(latitude, longitude, radius, start_date, end_date):
    results = terzo_requisito_query(driver, latitude, longitude, radius, start_date, end_date)

    df = create_dataframe(results)

    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

    tabulati_dir = os.path.join(os.getcwd(), "tabulati")
    create_directory(tabulati_dir)

    tabulati_coordinate_date_dir = os.path.join(tabulati_dir, "tabulati_coordinate_date")
    create_directory(tabulati_coordinate_date_dir)
    start_date= start_date.replace(':', '-')
    end_date = end_date.replace(':', '-')
    csv_filename = f"{latitude}_{longitude}_{radius}_{start_date}_{end_date}_people.csv"
    csv_path = os.path.join(tabulati_coordinate_date_dir, csv_filename)

    df.to_csv(csv_path, index=False)
    print(f"\nFile CSV '{csv_filename}' creato nella directory: {tabulati_coordinate_date_dir}")

if __name__ == "__main__":
    latitude = 45.95969977582438
    longitude = 9.365010069276185
    radius = 40

    start_date = "2024-07-1T00:00:00"
    end_date = "2024-07-19T00:00:10"

    return_results_three(latitude, longitude, radius, start_date, end_date)

    driver.close()