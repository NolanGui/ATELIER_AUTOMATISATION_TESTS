import sqlite3
import json
import os

# Le nom du fichier qui va stocker nos données
DB_FILE = "runs_history.db"

def init_db():
    """Crée la table de la base de données si elle n'existe pas déjà."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # On crée une table 'runs' avec 3 colonnes : id, timestamp, et data (qui contiendra le JSON)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_run(run_data):
    """Sauvegarde les résultats d'un test dans la base de données."""
    init_db() # On s'assure que la table existe
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # On extrait la date et on transforme le dictionnaire en texte (JSON)
    timestamp = run_data.get("timestamp", "")
    json_data = json.dumps(run_data)
    
    # On insère la nouvelle ligne dans la base
    cursor.execute('INSERT INTO runs (timestamp, data) VALUES (?, ?)', (timestamp, json_data))
    conn.commit()
    conn.close()

def list_runs(limit=10):
    """Récupère l'historique des derniers runs (du plus récent au plus ancien)."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # On va chercher les dernières lignes, triées par ID décroissant
    cursor.execute('SELECT data FROM runs ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    # On reconvertit le texte de la base de données en dictionnaires Python
    runs = []
    for row in rows:
        runs.append(json.loads(row[0]))
        
    return runs