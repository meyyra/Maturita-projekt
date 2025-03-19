from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Konfigurace databáze
DB_CONFIG = {
    "host": "dbs.spskladno.cz",
    "user": "student8",
    "password": "spsnet",
    "database": "vyuka8",
}

# Připojení k databázi
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# ----------------------- KATEGORIE & PRODUKTY -----------------------

@app.route("/categories")
def get_categories():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nazev FROM 1Akategorie ORDER BY id ASC")
    categories = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(categories)

@app.route("/products/<int:category_id>")
def get_products(category_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT nazev, cena FROM 1Aprodukty WHERE kategorie_id = %s", (category_id,))
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(products)

# ----------------------- SERVER -----------------------

if __name__ == "__main__":
    app.run(debug=True)
