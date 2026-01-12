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
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    query = "SELECT id, food_type, quantity, expiration, location, email FROM offers WHERE active=1 AND expiration > ?"
    params = [now]
    
    if criteria.get('food_type'):
        # Split into words and require at least one match (better relevance)
        words = criteria['food_type'].lower().split()
        conditions = " OR ".join(["LOWER(food_type) LIKE ?" for _ in words])
        query += f" AND ({conditions})"
        params.extend([f"%{w}%" for w in words])
    
    if criteria.get('quantity'):
        query += " AND quantity >= ?"
        params.append(criteria['quantity'])
    
    if criteria.get('location'):
        query += " AND LOWER(location) LIKE ?"
        params.append(f"%{criteria['location'].lower()}%")
    
    # Optional: sort by soonest expiring first
    query += " ORDER BY expiration ASC"
    
    c.execute(query, params)
    matches = c.fetchall()
    conn.close()
    return matches