# FoodieBot: A Database-Driven Conversational AI Food Agent 🍔🤖

FoodieBot is an intelligent conversational AI system designed to simulate a real-time, database-driven fast-food ordering experience. The bot analyzes user conversations in natural language to understand preferences, dietary needs, and budget. It calculates a real-time "interest score" and recommends personalized food items from a pre-generated database.

The entire system is built with a separate backend API (Flask) and a user-friendly web interface (Streamlit) that includes a live analytics dashboard.

## Core Features ✨

* **🤖 AI-Powered Data Generation:** The project begins by using a Large Language Model (LLM) to generate a comprehensive dataset of 100 unique fast-food products across 10 categories.
* **🧠 Intelligent Conversational Engine:** FoodieBot engages in natural dialogue to extract key information like dietary restrictions, budget, mood, and cravings.
* **📈 Real-Time Interest Scoring:** A dynamic interest score (0-100%) is calculated and updated with every user interaction, gauging their likelihood to purchase.
* **💾 Database-Driven Recommendations:** All product recommendations are queried in real-time from an SQLite database based on the user's extracted preferences.
* **📊 Live Analytics Dashboard:** The user interface includes a dashboard that tracks conversation metrics, such as the interest score progression over time and the most frequently recommended products.

## System Architecture ⚙️

The application operates with a decoupled frontend and backend architecture:
```
+--------------------------+      +-----------------------+      +------------------------+
|   User Interface         |      |   Backend API         |      |    Database & AI       |
|   (Streamlit)            | <--> |   (Flask)             | <--> |    (SQLite & LLM)      |
+--------------------------+      +-----------------------+      +------------------------+
        |                                   |                              |
- Renders chat UI & dashboard     - Handles /chat & /analytics  - Stores 100 products
- Sends user input to backend       endpoints                   - Logs conversations
- Displays bot responses          - Processes logic             - LLM for NLU & generation
                                  - Queries database
```

## Tech Stack 🛠️

* **Backend:** Flask
* **Frontend:** Streamlit
* **Database:** SQLite
* **LLM API:** Google Gemini (for data generation and conversational intelligence)
* **Python Libraries:** `requests`, `pandas`, `python-dotenv`

## Setup and Installation 🚀

Follow these steps to get FoodieBot running on your local machine.

**1. Prerequisites:**
* Python 3.9+
* A Google Gemini API Key

**2. Clone the Repository:**
```bash
git clone <https://github.com/RishabhAnand0325/FoodieBot.git>
cd FoodieBot
```

**3. Project Structure:**
```
/FoodieBot
|
|-- /data/
|   |-- foodiebot.db        # SQLite database for products and logs
|   |-- products.json       # AI-generated raw product data
|
|-- config.py               # Loads API keys and configurations
|-- generate_data.py        # Script to generate the 100 food products
|-- database_setup.py       # Script to create and populate the database
|-- core_logic.py           # Handles interest scoring, LLM calls, and DB queries
|-- app.py                  # The Flask backend API server
|-- ui.py                   # The Streamlit frontend web application
|-- requirements.txt        # List of Python dependencies
|-- .env                    # (You create this) For storing API keys
|-- README.md               # This file
```

**4. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**5. Configure API Key:**
Create a new file named .env in the root of the project directory and add your API key
```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

**6.Generate Product Data:**
Run the data generation script. This will make 100 calls to the LLM API and may take a few minutes.
```bash
python generate_data.py
```
This will create a products.json file inside the /data directory

**7. Set Up the Database:**
Run the database setup script to create and populate foodiebot.db.
```bash
python database_setup.py
```

## How to Run the Application ▶️

You need to run the backend and frontend in two separate terminals

**1. Start the Backend API (Terminal 1):**
```bash
flask --app app run --port 5001
```
Keep this terminal running

**2. Start the Frontend UI (Terminal 2):**
```bash
streamlit run ui.py
```
Your web browser should automatically open with the FoodieBot chat interface. You can now start chatting!
