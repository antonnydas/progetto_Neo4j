# progetto_Neo4j

# Scopo
Creazione di un metodo di ricerca tramite query che vada a soddisfare le richieste di ricerca tramite nome, data e ora, cella e coordinate geografiche e che restituisca i soggetti sospetti collegati. 

1. **Clona il repository**:
   - git  clone <URL del repository>

2. **Crea un ambiente Conda**:

   conda create --name infgpt python=3.12
   conda activate infgpt

3. **Installa le le librerie nell'ambiente**:
   
    - pip install os
    - pip install neo4j
    - pip install datetime
    - pip install time
    - pip install pandas
    - pip install tabulate
    - pip install collections
    - pip install Faker
    - pip install random
    - pip install math

4.**Creare l'instance**
   - Andare su neo4j aura e creare un'instance e salvarsi uri e password

5. **Inserire Credenziali**

   - Aprire il file "utilities.py", nella funzione connect_to_db il proprio uri e in AUTH lo         user e la password che sono      stati creati alla creazione dell'istance su neo4j aura.

   - Inserire nel file "create_db.py" l'uri presente con quello della propria instance creata.
  
   - Inserire nel file "main.py" l'uri presente con quello della propria instance creata e in        AUTH lo user e la password.

6. **Creazione DataBase**
   - Avviare il file "create_db.py" per la creazione del database con i vari nodi: persone,     
     Numeri di Telefono(NTel), celle, i punti geografici e le relazioni.

7. **Avviare la ricerca**
   - Aprire il file "main.py" e avviarlo per poter usare il menù di ricerca dei sospettati.
   

   


    
