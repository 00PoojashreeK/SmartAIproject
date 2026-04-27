import streamlit as st
import pandas as pd
import os

USER_FILE="users.csv"

def register():

    st.subheader("Register")

    username=st.text_input("Username")
    password=st.text_input("Password",type="password")

    if st.button("Register"):

        if os.path.exists(USER_FILE):
            users=pd.read_csv(USER_FILE)
        else:
            users=pd.DataFrame(columns=["username","password"])

        if username in users["username"].values:

            st.error("User already exists")

        else:

            new_user=pd.DataFrame([[username,password]],columns=["username","password"])

            users=pd.concat([users,new_user],ignore_index=True)

            users.to_csv(USER_FILE,index=False)

            st.success("Registration successful")

def login():

    st.subheader("Login")

    username=st.text_input("Username")
    password=st.text_input("Password",type="password")

    if st.button("Login"):

        if not os.path.exists(USER_FILE):
            st.error("No users registered")
            return

        users=pd.read_csv(USER_FILE)

        if ((users["username"]==username)&(users["password"]==password)).any():

            st.session_state.logged_in=True

            st.success("Login successful")

        else:
            st.error("Invalid credentials")