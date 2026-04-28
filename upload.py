import streamlit as st
import pandas as pd
import os

def app():

    st.header("Upload Dataset")

    file=st.file_uploader("Upload CSV Dataset",type=["csv"])

    if file is not None:

        df=pd.read_csv(file)

        df.to_csv("dataset.csv",index=False)

        st.success("Dataset uploaded successfully")

        st.dataframe(df.head())

    if os.path.exists("dataset.csv"):

        df=pd.read_csv("dataset.csv")

        st.subheader("Current Dataset")

        st.dataframe(df.head())