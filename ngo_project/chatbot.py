import streamlit as st
import pandas as pd
import os
import google.genai as genai
from dotenv import load_dotenv
import traceback


# ---------- Load API Key ----------
load_dotenv()

# Try to get API key from Streamlit secrets first (for Cloud deployment)
# Then fall back to .env file (for local development)
api_key = None

try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except:
    api_key = os.getenv("GEMINI_API_KEY")

# Validate API key
if not api_key or api_key == "your_gemini_api_key_here":
    st.error("""
    ❌ GEMINI_API_KEY not configured
    
    **For local development:**
    1. Open `.env` file in ngo_project folder
    2. Add your Gemini API key: `GEMINI_API_KEY=your_key_here`
    3. Get it from: https://aistudio.google.com/app/apikey
    
    **For Streamlit Cloud deployment:**
    1. Go to your app settings on Streamlit Cloud
    2. Click "Secrets" in the sidebar
    3. Add: `GEMINI_API_KEY = your_key_here`
    """)
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini API: {str(e)}")
    st.stop()


def app():

    st.title("🤖 AI Disaster Chatbot")

    if not os.path.exists("dataset.csv"):
        st.warning("Upload dataset first")
        return

    df = pd.read_csv("dataset.csv")

    # Convert dataset into text context for AI
    dataset_context = df.to_string(index=False)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask anything about disasters, NGOs, or the dataset...")

    if prompt:

        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        # AI prompt with dataset context
        ai_prompt = f"""
You are an AI assistant for NGO disaster management.

Here is the dataset containing disaster information:

{dataset_context}

User Question:
{prompt}

Answer clearly and provide helpful recommendations if possible.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ai_prompt
            )
            ai_reply = response.text

        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            st.error(error_msg)
            print(f"Chatbot Error: {traceback.format_exc()}")
            ai_reply = "⚠️ AI service temporarily unavailable. Please try again."

        # Store assistant reply
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

        with st.chat_message("assistant"):
            st.write(ai_reply)