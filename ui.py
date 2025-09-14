# ui.py
import streamlit as st
import requests
import uuid
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="FoodieBot 🍔",
    page_icon="🤖",
    layout="wide"
)

# --- API Endpoint ---
BACKEND_URL = "http://127.0.0.1:5001"

# --- Session State Initialization ---
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.interest_score = 0
    st.session_state.initial_greeting = True

# --- UI Components ---
st.title("FoodieBot AI 🍕")
st.markdown("Your personal AI agent for fast food cravings!")

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    # --- Chat Interface --- [cite: 143]
    st.header("Chat with FoodieBot")

    if st.session_state.initial_greeting:
        greeting = "Welcome to FoodieBot! What's your food mood today? 😋"
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.session_state.initial_greeting = False

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "product" in message and message["product"]:
                p = message["product"]
                with st.container(border=True):
                    st.subheader(p['name'])
                    st.caption(f"Category: {p['category']} | Price: ${p['price']:.2f}")
                    st.write(p['description'])
                    st.progress(p['popularity_score'], text=f"Popularity: {p['popularity_score']}%")


    # React to user input
    if prompt := st.chat_input("I'm looking for something spicy..."):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call backend API
        with st.spinner("FoodieBot is thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "message": prompt,
                    "session_id": st.session_state.session_id,
                    "interest_score": st.session_state.interest_score
                }
            )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.interest_score = data['interest_score']
            bot_response = data['bot_response']
            product = data['recommended_product']
            
            # Display bot response
            with st.chat_message("assistant"):
                st.markdown(bot_response)
                # Display recommended product card [cite: 145]
                if product:
                    with st.container(border=True):
                        st.subheader(product['name'])
                        st.caption(f"Category: {product['category']} | Price: ${product['price']:.2f}")
                        st.write(product['description'])
                        st.progress(product['popularity_score'], text=f"Popularity: {product['popularity_score']}%")

            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_response,
                "product": product
            })
        else:
            st.error("Sorry, something went wrong. Please try again.")
        
        # Rerun to update the analytics pane immediately
        st.rerun()

with col2:
    # --- Real-time Analytics Dashboard --- [cite: 105]
    st.header("Live Analytics")

    # Display Interest Score [cite: 144]
    st.metric(label="User Interest Score", value=f"{st.session_state.interest_score}%")
    st.progress(st.session_state.interest_score)
    
    st.markdown("---")
    
    # Fetch and display analytics data
    analytics_response = requests.get(
        f"{BACKEND_URL}/analytics",
        params={"session_id": st.session_state.session_id}
    )

    if analytics_response.status_code == 200:
        analytics_data = analytics_response.json()

        # Interest Score Progression Graph [cite: 109]
        st.subheader("Interest Score Over Time")
        interest_df = pd.DataFrame(analytics_data['interest_progression'])
        if not interest_df.empty:
            interest_df.set_index('id', inplace=True)
            st.line_chart(interest_df)
        else:
            st.write("No conversation data yet to plot.")

        # Top Recommended Products [cite: 115]
        st.subheader("Most Recommended Products")
        recs_df = pd.DataFrame(analytics_data['top_recommendations'])
        if not recs_df.empty:
            st.bar_chart(recs_df.set_index('name'))
        else:
            st.write("No recommendations have been made yet.")
            