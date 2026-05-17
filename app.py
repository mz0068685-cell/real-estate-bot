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
            
        # --- CHAT MEMORY INTIALIZATION ---
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        st.write("Ask me anything about properties in Dubai, London (UK), Paris (Europe), Istanbul, or New York!")
        
        # Display previous chat messages
        for role, text in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"*👤 You:* {text}")
            else:
                st.markdown(f"*🤖 AI:* {text}")
        
        # Form for user input to prevent automatic page reload on typing
        with st.form(key="chat_form", clear_on_submit=True):
            user_question = st.text_input("Your Question:")
            submit_button = st.form_submit_button(label="Send")
            
        if submit_button and user_question:
            # Append user question to history
            st.session_state.chat_history.append(("user", user_question))
            
            # Prepare context from CSV file and history
            context = df.to_string()
            
            # Format history for AI context
            history_str = ""
            for role, text in st.session_state.chat_history[:-1]:
                history_str += f"{role}: {text}\n"
                
            prompt = f"You are a professional real estate agent assistant. Use the following property data and previous conversation history to answer the current question accurately. If the info is not in data, reply politely.\n\nData:\n{context}\n\nHistory:\n{history_str}\n\nCurrent Question: {user_question}"
            
            # Call the Latest Gemini Model
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Append AI response to history
            st.session_state.chat_history.append(("ai", response.text))
            
            # Rerun the app to show the new message instantly
            st.rerun()
            
    except FileNotFoundError:
        st.error("Please create and upload the 'properties.csv' file first.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Gemini API Key in the sidebar to start.")
