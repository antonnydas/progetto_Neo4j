# Funzione richiesta LIV.2
def find_people_connected_to_cell(driver, cell_id, date, time):
    def find_people_by_cell_and_time(tx):
        query = """
        MATCH (p:Persona)-[:POSSEDUTO_DA]->(n:N_Tel)-[r:CONNESSO_A]->(c:Cella {id: $cell_id})
        WHERE $date >= r.data_inizio AND $date <= r.data_fine
        AND $time >= r.orario_inizio AND $time <= r.orario_fine
        RETURN p.nome AS person_name, n.id AS sim_id
        """
        result = tx.run(query, cell_id=cell_id, date=date, time=time)
        return [{"person_name": record["person_name"], "sim_id": record["sim_id"]} for record in result]

    with driver.session() as session:
        return session.read_transaction(find_people_by_cell_and_time)

# Funzione richiesta LIV.3
def get_persons_near_coordinates(driver, latitude, longitude, radius, date, time):
    def find_persons_by_location_and_time(tx):
        query = """
        WITH point({latitude: $latitude, longitude: $longitude}) AS center
        MATCH (c:Cella)
        WHERE distance(point({latitude: c.latitude, longitude: c.longitude}), center) <= $radius
        WITH c
        MATCH (p:Persona)-[:POSSEDUTO_DA]->(n:N_Tel)-[r:CONNESSO_A]->(c)
        WHERE date($date) >= r.data_inizio AND date($date) <= r.data_fine
        AND time($time) >= r.orario_inizio AND time($time) <= r.orario_fine
        RETURN p.nome AS person_name, n.id AS sim_id, c.nome AS cell_name, c.posizione AS cell_location
        """
        result = tx.run(query, latitude=latitude, longitude=longitude, radius=radius, date=date, time=time)
        return [{"person_name": record["person_name"], "sim_id": record["sim_id"], "cell_name": record["cell_name"], "cell_location": record["cell_location"]} for record in result]

    with driver.session() as session:
        return session.read_transaction(find_persons_by_location_and_time)
        
