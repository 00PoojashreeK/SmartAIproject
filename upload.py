import streamlit as st
import pandas as pd
import os

def app():

    st.title("📂 Upload Dataset")

    file=st.file_uploader("Upload CSV",type=["csv"])

    if file:

        df=pd.read_csv(file)
        df.to_csv("dataset.csv",index=False)

        st.success("Dataset uploaded")

    if os.path.exists("dataset.csv"):

        df=pd.read_csv("dataset.csv")

        st.subheader("Current Dataset")

        st.dataframe(df,use_container_width=True)

        if st.button("Delete Dataset"):

            os.remove("dataset.csv")

            st.success("Dataset deleted")

            st.rerun()