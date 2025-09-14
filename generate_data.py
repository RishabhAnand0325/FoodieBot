# generate_data.py

 # "Sides & Appetizers (fries, onion rings, etc.)", "Beverages (sodas, shakes, specialty drinks)",
    # "Desserts (ice cream, cookies, pastries)", "Salads & Healthy Options",
    # "Breakfast Items (all-day breakfast)", "Limited Time Specials"
    
import os
import json
import time
import google.generativeai as genai
from config import API_KEY

# Configure the generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

PRODUCT_CATEGORIES = [
    "Burgers (classic, fusion, vegetarian)", "Pizza (traditional, gourmet, personal)",
    "Fried Chicken (wings, tenders, sandwiches)", "Tacos & Wraps (mexican, fusion, healthy)",
   
]

def generate_products():
    """Generates 100 fast food products using the LLM API and saves them to a JSON file."""
    all_products = []
    
    # Generate 10 products for each category
    for category in PRODUCT_CATEGORIES:
        print(f"Generating 10 products for category: {category}...")
        for i in range(10):
            # Construct a detailed prompt
            prompt = f"""
            Generate a JSON object for a single, unique fast food product for the category '{category}'.
            The product name must be creative and sound appealing.
            The description should be enticing and short (20 words max).
            Ensure the structure exactly matches this format, including all fields:
            {{
              "product_id": "string",
              "name": "string",
              "category": "{category.split(' ')[0]}",
              "description": "string",
              "ingredients": ["string", "string", ...],
              "price": float (e.g., 12.99),
              "calories": integer,
              "prep_time": "string (e.g., 8-10 mins)",
              "dietary_tags": ["string", "string", ...],
              "mood_tags": ["string", "string", ...],
              "allergens": ["string", "string", ...],
              "popularity_score": integer (1-100),
              "chef_special": boolean,
              "limited_time": boolean,
              "spice_level": integer (0-10),
              "image_prompt": "string (a descriptive prompt for an image generator)"
            }}
            Do NOT include the markdown "```json" wrapper in your response.
            """
            
            try:
                response = model.generate_content(prompt)
                # Clean up the response to extract only the JSON part
                cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
                product_data = json.loads(cleaned_response)
                
                # Assign a unique ID
                product_data['product_id'] = f"FF{len(all_products) + 1:03d}"
                all_products.append(product_data)
                print(f"  -> Generated: {product_data['name']}")
                time.sleep(2) # To avoid hitting API rate limits
            except (json.JSONDecodeError, Exception) as e:
                print(f"An error occurred: {e}. Retrying...")
                i -= 1 # Retry the current iteration
                time.sleep(5)

    # Save to file
    output_path = os.path.join('data', 'products.json')
    os.makedirs('data', exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(all_products, f, indent=2)
        
    print(f"\nSuccessfully generated {len(all_products)} products and saved to {output_path}")

if __name__ == "__main__":
    generate_products()