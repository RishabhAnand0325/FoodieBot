# database_setup.py
import sqlite3
import json
import os

DB_PATH = os.path.join('data', 'foodiebot.db')
JSON_PATH = os.path.join('data', 'products.json')

def create_database():
    """Creates the database schema for products, conversations, and analytics."""
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop tables if they exist for a clean setup
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS conversation_history")

    # Create Products Table [cite: 154]
    cursor.execute("""
    CREATE TABLE products (
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        description TEXT,
        ingredients TEXT,
        price REAL,
        calories INTEGER,
        prep_time TEXT,
        dietary_tags TEXT,
        mood_tags TEXT,
        allergens TEXT,
        popularity_score INTEGER,
        chef_special BOOLEAN,
        limited_time BOOLEAN,
        spice_level INTEGER,
        image_prompt TEXT
    )
    """)

    # Create Conversation History Table [cite: 146]
    cursor.execute("""
    CREATE TABLE conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL, -- 'user' or 'bot'
        content TEXT,
        interest_score INTEGER,
        recommendation_made TEXT, -- product_id of recommended item
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create indexes for efficient querying [cite: 135]
    cursor.execute("CREATE INDEX idx_category ON products (category)")
    cursor.execute("CREATE INDEX idx_price ON products (price)")
    cursor.execute("CREATE INDEX idx_popularity ON products (popularity_score)")


    print("Database schema created successfully.")
    conn.commit()
    conn.close()

def populate_products():
    """Populates the products table from the generated JSON file."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(JSON_PATH, 'r') as f:
        products = json.load(f)

    for product in products:
        # Convert lists to JSON strings for storage
        for key in ['ingredients', 'dietary_tags', 'mood_tags', 'allergens']:
            if isinstance(product.get(key), list):
                product[key] = json.dumps(product[key])
        
        cursor.execute("""
        INSERT INTO products (
            product_id, name, category, description, ingredients, price,
            calories, prep_time, dietary_tags, mood_tags, allergens,
            popularity_score, chef_special, limited_time, spice_level, image_prompt
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(product.values()))

    print(f"Successfully populated the database with {len(products)} products.")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    populate_products()