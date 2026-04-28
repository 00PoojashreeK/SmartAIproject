import streamlit as st
import pandas as pd
import os

def app():

    st.title("🤖 AI Disaster Chatbot")

    if not os.path.exists("dataset.csv"):
        st.warning("Upload dataset first")
        return

    df=pd.read_csv("dataset.csv")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt=st.chat_input("Ask anything")

    if prompt:

        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.write(prompt)

        response="I am an AI assistant for NGO disaster management."

        if "people" in prompt.lower():
            response=f"Total people needing help: {df['People_in_need'].sum()}"

        if "volunteer" in prompt.lower():
            response=f"Total volunteers: {df['Volunteers'].sum()}"

        st.session_state.messages.append({"role":"assistant","content":response})

        with st.chat_message("assistant"):
            st.write(response)