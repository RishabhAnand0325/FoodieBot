# core_logic.py
import sqlite3
import json
import os
import google.generativeai as genai
from config import API_KEY

# Configure the LLM
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

DB_PATH = os.path.join('data', 'foodiebot.db')

# --- Interest Scoring Logic --- [cite: 51]
ENGAGEMENT_FACTORS = {
    'specific_preferences': 15, 'dietary_restrictions': 10, 'budget_mention': 5,
    'mood_indication': 20, 'question_asking': 10, 'enthusiasm_words': 8,
    'price_inquiry': 25, 'order_intent': 30
}
NEGATIVE_FACTORS = {
    'hesitation': -10, 'budget_concern': -15,
    'dietary_conflict': -20, 'rejection': -25, 'delay_response': -5
}

def calculate_interest_score(text, current_score):
    """Calculates the interest score based on keywords in the user's message."""
    score_change = 0
    text_lower = text.lower()
    
    # Positive keywords
    if any(k in text_lower for k in ["love", "want", "need", "perfect", "amazing", "great"]): score_change += ENGAGEMENT_FACTORS['enthusiasm_words']
    if any(k in text_lower for k in ["how much", "price", "cost"]): score_change += ENGAGEMENT_FACTORS['price_inquiry']
    if any(k in text_lower for k in ["i'll take it", "add to cart", "order", "buy"]): score_change += ENGAGEMENT_FACTORS['order_intent']
    if any(k in text_lower for k in ["what's in", "spice level", "calories"]): score_change += ENGAGEMENT_FACTORS['question_asking']

    # Negative keywords
    if any(k in text_lower for k in ["maybe", "not sure", "i guess"]): score_change += NEGATIVE_FACTORS['hesitation']
    if any(k in text_lower for k in ["too expensive", "that's a lot"]): score_change += NEGATIVE_FACTORS['budget_concern']
    if any(k in text_lower for k in ["don't like", "no thanks", "not that"]): score_change += NEGATIVE_FACTORS['rejection']
    
    new_score = max(0, min(100, current_score + score_change))
    return new_score

# --- Conversational Intelligence & Database Integration --- [cite: 43]
def extract_preferences_from_conversation(history):
    """Uses LLM to extract structured data from conversation."""
    prompt = f"""
    Analyze the following user conversation history and extract their food preferences into a JSON object.
    Identify: budget (as a max price float), mood (list of strings), cravings/keywords (list of strings), and dietary restrictions (list of strings).
    If a preference is not mentioned, omit the key.
    
    CONVERSATION:
    {history}
    
    JSON:
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_response)
    except Exception:
        return {} # Return empty dict if parsing fails

def query_database_for_products(preferences):
    """Searches the database for products matching the user's preferences."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    cursor = conn.cursor()
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if preferences.get("budget"):
        query += " AND price <= ?"
        params.append(preferences["budget"])
    
    # Build dynamic query for tags [cite: 99]
    search_tags = preferences.get("mood", []) + preferences.get("cravings", []) + preferences.get("dietary", [])
    for tag in search_tags:
        query += " AND (mood_tags LIKE ? OR dietary_tags LIKE ? OR name LIKE ? OR description LIKE ?)"
        param_like = f'%"{tag}"%' # For JSON arrays stored as strings
        params.extend([param_like, param_like, f'%{tag}%', f'%{tag}%'])

    query += " ORDER BY popularity_score DESC LIMIT 5"
    
    cursor.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products

def generate_bot_response(history, products):
    """Generates a natural, friendly response using the LLM based on recommended products."""
    product_str = "No specific products found, just chat with the user."
    if products:
        product_str = "Here are the top products found that match the user's request:\n"
        for p in products:
            product_str += f"- {p['name']}: {p['description']} (Price: ${p['price']})\n"

    prompt = f"""
    You are FoodieBot, a friendly and enthusiastic fast food expert.
    Your goal is to help a user find the perfect meal.
    Based on the conversation history and the products found in the database, generate a short, engaging response.
    
    - If there are good matches, highlight the best one (the first in the list).
    - Ask a clarifying question to keep the conversation going.
    - DO NOT list all the products. Just mention the top one and maybe hint that there are others.
    - Keep your response under 50 words.

    CONVERSATION HISTORY:
    {history}

    PRODUCTS FOUND:
    {product_str}
    
    YOUR RESPONSE:
    """
    response = model.generate_content(prompt)
    return response.text.strip()