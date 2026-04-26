import streamlit as st
import google.generativeai as genai
import assistant

# 1. Setup Gemini with the 2026 Model discovered in check_models.py
try:
    # Pull the key from .streamlit/secrets.toml
    raw_key = st.secrets["GEMINI_API_KEY"]
    # Clean the key to prevent hidden character errors
    clean_key = raw_key.strip().replace('"', '').replace("'", "")
    
    genai.configure(api_key=clean_key)
except Exception as e:
    st.error(f"Secret Error: {e}. Check your .streamlit/secrets.toml file!")

def ask_chatbot(user_question):
    try:
        # 2. Get the Source-Aware prompt (Rules from Day 6 + Data from Day 5)
        full_prompt = assistant.generate_source_aware_prompt(user_question)
        
        # 3. Initialize the EXACT model from your discovery list
        # Using 2.5-flash as it is the most stable 2026 workhorse
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # 4. Generate the response
        response = model.generate_content(full_prompt)
        
        # Return the AI's text answer
        return response.text
        
    except Exception as e:
        # If the API versioning trips up again, this will tell us
        return f"I'm having trouble connecting to my Gemini brain. Error: {e}"

if __name__ == "__main__":
    # Test script for terminal use
    test_query = "What help is available for housing?"
    print(f"Testing Gemini 2.5 with: {test_query}")
    print(ask_chatbot(test_query))