import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
import traceback


# ---------- Load API Key ----------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Validate API key
if not api_key or api_key == "your_gemini_api_key_here":
    st.error("❌ GEMINI_API_KEY not configured in .env file")
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
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
            response = model.generate_content(ai_prompt)
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