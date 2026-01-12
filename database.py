import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS offers
                 (id INTEGER PRIMARY KEY, food_type TEXT, quantity INTEGER, expiration TEXT, location TEXT, email TEXT, active INTEGER DEFAULT 1)''')
    conn.commit()
    conn.close()

def add_offer(food_type, quantity, expiration, location, email):
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    c.execute("INSERT INTO offers (food_type, quantity, expiration, location, email) VALUES (?, ?, ?, ?, ?)",
              (food_type, quantity, expiration, location, email))
    conn.commit()
    conn.close()

def get_active_offers():
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    now = datetime.now().isoformat()
    # Deactivate expired offers
    c.execute("UPDATE offers SET active=0 WHERE expiration < ? AND active=1", (now,))
    conn.commit()
    # Get active ones
    c.execute("SELECT * FROM offers WHERE active=1")
    offers = c.fetchall()
    conn.close()
    return offers

def match_offers(criteria):
    # criteria is a dict from Gemini, e.g., {'food_type': 'vegetarian', 'quantity': 15, 'location': 'Abuja', 'max_expiration': '2026-01-11T20:00:00'}
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    now = datetime.now().isoformat()
    query = "SELECT * FROM offers WHERE active=1 AND expiration > ?"
    params = [now]
    
    if 'food_type' in criteria:
        query += " AND food_type LIKE ?"
        params.append(f"%{criteria['food_type']}%")
    if 'quantity' in criteria:
        query += " AND quantity >= ?"
        params.append(criteria['quantity'])
    if 'location' in criteria:
        query += " AND location LIKE ?"
        params.append(f"%{criteria['location']}%")
    if 'max_expiration' in criteria:
        query += " AND expiration <= ?"
        params.append(criteria['max_expiration'])
    
    c.execute(query, params)
    matches = c.fetchall()
    conn.close()
    return matches