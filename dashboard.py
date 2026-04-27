import streamlit as st
import pandas as pd
import os

def app():

    st.header("Dashboard")

    if not os.path.exists("dataset.csv"):

        st.warning("Upload dataset first")

        return

    df=pd.read_csv("dataset.csv")

    st.write("Rows:",df.shape[0])
    st.write("Columns:",df.shape[1])

    st.dataframe(df)

    st.subheader("Column Types")

    st.write(df.dtypes)