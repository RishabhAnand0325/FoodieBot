# app.py
from flask import Flask, request, jsonify
import sqlite3
import json
import uuid
from core_logic import (
    calculate_interest_score,
    extract_preferences_from_conversation,
    query_database_for_products,
    generate_bot_response
)

app = Flask(__name__)
DB_PATH = 'data/foodiebot.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_conversation_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM conversation_history WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    )
    history = cursor.fetchall()
    conn.close()
    return "\n".join([f"{row['role']}: {row['content']}" for row in history])

def log_message(session_id, role, content, score, recommendation=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO conversation_history 
           (session_id, role, content, interest_score, recommendation_made) 
           VALUES (?, ?, ?, ?, ?)""",
        (session_id, role, content, score, recommendation)
    )
    conn.commit()
    conn.close()


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    session_id = data.get('session_id')
    current_score = int(data.get('interest_score', 0))

    if not session_id:
        session_id = str(uuid.uuid4())

    # 1. Log user message & update score
    log_message(session_id, 'user', user_message, current_score)
    new_score = calculate_interest_score(user_message, current_score)

    # 2. Build conversation context
    history = get_conversation_history(session_id)
    
    # 3. Conversational Intelligence [cite: 43]
    preferences = extract_preferences_from_conversation(history)
    
    # 4. Database Query [cite: 79]
    products = query_database_for_products(preferences)
    
    # 5. Recommendation & Response Generation
    bot_response_text = generate_bot_response(history, products)
    
    # 6. Log bot response
    recommended_product = products[0] if products else None
    log_message(session_id, 'bot', bot_response_text, new_score, recommended_product['product_id'] if recommended_product else None)

    return jsonify({
        'session_id': session_id,
        'bot_response': bot_response_text,
        'interest_score': new_score,
        'recommended_product': recommended_product
    })

@app.route('/analytics', methods=['GET'])
def analytics():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400
        
    conn = get_db_connection()
    # Interest score progression [cite: 109]
    scores = conn.execute(
        "SELECT id, interest_score FROM conversation_history WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    ).fetchall()
    
    # Most recommended products [cite: 115]
    recs = conn.execute(
        """SELECT p.name, COUNT(h.recommendation_made) as count 
           FROM conversation_history h
           JOIN products p ON h.recommendation_made = p.product_id
           GROUP BY p.name ORDER BY count DESC LIMIT 5"""
    ).fetchall()

    conn.close()

    return jsonify({
        'interest_progression': [dict(row) for row in scores],
        'top_recommendations': [dict(row) for row in recs]
    })


if __name__ == '__main__':
    app.run(port=5001, debug=True)