# progetto_Neo4j

## Obiettivo: 
Creazione di un metodo di ricerca tramite query che vada a soddisfare le richieste di ricerca tramite nome, data e ora,
cella e coordinate geografiche e che restituisca i soggetti sospetti collegati.

### 1. **Clona il repository**:
`git clone <URL del repository>`

### 2. **Crea un ambiente Conda**:
   `conda create --name neo4j python=3.12 `

`conda activate neo4j`

### 3. **Installa le le librerie nell'ambiente**:
`pip install -r requirements.txt`

### 4. **Creare l'instance**

1. Accedere a questo URL: https://neo4j.com/cloud/platform/aura-graph-database/
2. Premere sul tasto "Start Free"
3. Cliccare su "New Instance", che vi fornirà le credenziali necessarie
4. aprire l'instnza creata

### 5. **Inserire Credenziali**

   #### ATTENZIONE: è necessario avere le credenziali che sono state fornite durante la creazione dell'istanza per i prossimi passaggi

-  Aprire il modulo `"utilities.py"`, nella funzione `connect_to_db` sostituire l'uri e l'AUTH presenti con quelli che sono
   stati scaricati durante la creazione dell'istanza.

-  Nel modulo `create_db.py` sostituire l'uri presente con quello della propria istanza creata.

-  Nel modulo `main.py` sostituire l'uri presente con quello della propria istanza e in AUTH lo user e la password.

### 6. **Creazione DataBase**
Avviare il file `create_db.py ` per la creazione del database con i vari nodi: Persone,     
Sim, Celle, i punti geografici e le relazioni.

### 7. **Avviare la ricerca**
Aprire il modulo `"main.py"` e avviarlo per poter usare il menù di ricerca dei sospettati.
   

   


    
