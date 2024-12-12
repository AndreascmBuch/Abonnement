import sqlite3
from flask import Flask, jsonify, request
import requests

# Opret forbindelse til databasen
def get_db_connection():
    conn = sqlite3.connect("Abonnement.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/abonnement', methods=['POST'])
def create_abonnement():
    data = request.json
    
    try:
        # Udpak data fra JSON
        kunde_id = data["kunde_id"]
        car_id = data["car_id"]
        term = data["term"]
        price_per_month = data["price_per_month"]
        start_month = data["start_month"]
        end_month = data["end_month"]
        restance = data["restance"]
        contract_information = data["contract_information"]

        # Tjek data fra kunde-mikroservice
        kunde_response = requests.get(f"https://kunde-api-dnecdehugrhmbghu.northeurope-01.azurewebsites.net/customers/{kunde_id}")
        if kunde_response.status_code != 200:
            return jsonify({"error": "Kunde ikke fundet"}), 404

        # Tjek data fra bil-mikroservice
        damage_response = requests.get(f"https://bildatabasedemo-hzfbegh6eqfraqdd.northeurope-01.azurewebsites.net/cars/{car_id}")
        if damage_response.status_code != 200:
            return jsonify({"error": "Skadesdata ikke fundet for bilen"}), 404

        # Indsæt data i databasen
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscription (
                kunde_id, car_id, term, price_per_month,
                start_month, end_month, restance, contract_information
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (kunde_id, car_id, term, price_per_month, start_month, end_month, restance, contract_information))
        conn.commit()
        conn.close()

        return jsonify({"message": "Abonnement oprettet succesfuldt"}), 201

    except KeyError as e:
        return jsonify({"error": f"Manglende nøgle: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Serverfejl: {str(e)}"}), 500


# test route så vi ikke får 404
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Abonnement",
        "version": "1.0.0",
        "description": "A RESTful API for managing abonnement"
    })


if __name__ == '__main__':
    app.run(debug=True)











