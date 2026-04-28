import streamlit as st
import pandas as pd
import os
import re

USER_FILE="users.csv"

def init_db():

    if not os.path.exists(USER_FILE):

        df=pd.DataFrame(columns=["name","email","password"])
        df.to_csv(USER_FILE,index=False)

def valid_email(email):

    pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern,email)

def register():

    init_db()

    st.subheader("Create Account")

    name=st.text_input("Full Name")
    email=st.text_input("Email")
    password=st.text_input("Password",type="password")
    confirm=st.text_input("Confirm Password",type="password")

    if st.button("Signup"):

        users=pd.read_csv(USER_FILE)

        if email in users["email"].values:
            st.error("User already exists")

        elif password!=confirm:
            st.error("Passwords do not match")

        elif not valid_email(email):
            st.error("Invalid email")

        else:

            new_user=pd.DataFrame([[name,email,password]],
            columns=["name","email","password"])

            users=pd.concat([users,new_user],ignore_index=True)

            users.to_csv(USER_FILE,index=False)

            st.success("Account created successfully")

def login():

    init_db()

    st.subheader("Login")

    email=st.text_input("Email")
    password=st.text_input("Password",type="password")

    if st.button("Login"):

        users=pd.read_csv(USER_FILE)

        user=users[(users["email"]==email)&(users["password"]==password)]

        if len(user)>0:

            st.session_state.logged_in=True
            st.session_state.user_email=email
            st.session_state.user_name=user.iloc[0]["name"]

            st.rerun()

        else:
            st.error("Invalid email or password")

def profile_sidebar():

    st.sidebar.title("👤 Profile")

    st.sidebar.write("Name:",st.session_state.user_name)
    st.sidebar.write("Email:",st.session_state.user_email)

    st.sidebar.divider()