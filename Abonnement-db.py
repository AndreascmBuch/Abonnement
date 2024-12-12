import sqlite3

# Opret forbindelse til databasen
conn = sqlite3.connect("Abonnement.db")
cursor = conn.cursor()

# Opret tabellen med abonnementsdata
cursor.execute('''
CREATE TABLE IF NOT EXISTS subscription (
    kunde_id INTEGER,
    car_id INTEGER,
    term INTEGER,
    price_per_month INTEGER,
    start_month DATETIME,
    end_month DATETIME,
    restance BOOLEAN,
    contract_information TEXT
)
''')



