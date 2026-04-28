import streamlit as st
import pandas as pd
import os

def app():

    st.header("Report")

    if not os.path.exists("dataset.csv"):

        st.warning("Upload dataset first")
        return

    df=pd.read_csv("dataset.csv")

    st.dataframe(df)

    st.write("Rows:",df.shape[0])
    st.write("Columns:",df.shape[1])

    csv=df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Report",
        csv,
        "ngo_report.csv",
        "text/csv"
    )