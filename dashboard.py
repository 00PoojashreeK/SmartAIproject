import streamlit as st
import pandas as pd
import os

def card(title,value):

    st.markdown(f"""
    <div class="card">
    <h3>{title}</h3>
    <h1>{value}</h1>
    </div>
    """,unsafe_allow_html=True)

def app():

    st.title("📊 NGO Disaster Dashboard")

    if not os.path.exists("dataset.csv"):
        st.warning("Upload dataset first")
        return

    df=pd.read_csv("dataset.csv")

    c1,c2,c3=st.columns(3)

    with c1:
        card("Locations",len(df))

    with c2:
        card("People in Need",df["People_in_need"].sum())

    with c3:
        card("Volunteers",df["Volunteers"].sum())

    st.divider()

    col1,col2=st.columns(2)

    with col1:
        st.subheader("People in Need")
        st.bar_chart(df["People_in_need"])

    with col2:
        st.subheader("Volunteers")
        st.bar_chart(df["Volunteers"])

    st.subheader("Dataset Preview")
    st.dataframe(df,use_container_width=True)