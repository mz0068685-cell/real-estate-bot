import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Global Real Estate AI Bot", layout="wide")
st.title("🏢 Global Real Estate AI Assistant")

# Sidebar for API Key & Data
st.sidebar.header("Setup Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    # Configure the Google Gemini API
    genai.configure(api_key=api_key)
    
    # Load Properties Data from CSV
    try:
        df = pd.read_csv("properties.csv")
        st.sidebar.success("Property data loaded successfully!")
        
        # Show properties in sidebar for reference if user wants
        if st.sidebar.checkbox("Show Available Properties"):
            st.sidebar.write(df)
            
        # Chat interface
        st.write("Ask me anything about properties in Dubai, London (UK), Paris (Europe), Istanbul, or New York!")
        user_question = st.text_input("Your Question (e.g., Tell me about the London property or European apartments):")
        
        if user_question:
            # Prepare context from CSV file
            context = df.to_string()
            prompt = f"You are a professional real estate agent assistant. Use the following property data to answer the user's question accurately. If the info is not in data, reply politely.\n\nData:\n{context}\n\nQuestion: {user_question}"
            
            # Call the Latest Gemini Model
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            st.subheader("AI Agent Response:")
            st.write(response.text)
            
    except FileNotFoundError:
        st.error("Please create and upload the 'properties.csv' file first.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Gemini API Key in the sidebar to start.")
