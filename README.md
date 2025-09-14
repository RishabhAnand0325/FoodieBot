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
- Renders chat UI & dashboard           - Handles /chat & /analytics endpoints - Stores 100 products
- Sends user input to backend           - Processes logic                - Logs conversations
- Displays bot responses                - Queries database               - LLM for NLU & generation
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
