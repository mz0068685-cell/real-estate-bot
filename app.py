import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="International Real Estate AI Bot", layout="wide")
st.title("🏢 International Real Estate AI Assistant")

# Sidebar for API Key & Data
st.sidebar.header("Setup Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Load Properties Data
    try:
        df = pd.read_csv("properties.csv")
        st.sidebar.success("Property data loaded successfully!")
        
        # Show properties in sidebar for reference
        if st.sidebar.checkbox("Show Available Properties"):
            st.sidebar.write(df)
            
        # Chat interface
        st.write("Ask me anything about Dubai, London, or New York properties!")
        user_question = st.text_input("Your Question (e.g., What is the price of the Dubai apartment?):")
        
        if user_question:
            # Prepare context from CSV
            context = df.to_string()
            prompt = f"You are a professional real estate agent assistant. Use the following property data to answer the user's question accurately. If the info is not in data, reply politely.\n\nData:\n{context}\n\nQuestion: {user_question}"
            
            # Call Gemini Model
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            st.subheader("AI Agent Response:")
            st.write(response.text)
            
    except FileNotFoundError:
        st.error("Please create and upload the 'properties.csv' file first.")
else:
    st.info("Please enter your Gemini API Key in the sidebar to start.")
