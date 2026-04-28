import streamlit as st
import auth
import upload
import dashboard
import ai_model
import map
import report

st.set_page_config(page_title="NGO Smart Resource Allocation System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False


if not st.session_state.logged_in:

    st.title("NGO Smart Resource Allocation System")

    option=st.selectbox("Select Option",["Login","Register"])

    if option=="Login":
        auth.login()

    else:
        auth.register()

else:

    st.sidebar.title("Navigation")

    menu=st.sidebar.radio(
        "Menu",
        ["Upload Dataset","Dashboard","AI Model","Map","Report","Logout"]
    )

    if menu=="Upload Dataset":
        upload.app()

    elif menu=="Dashboard":
        dashboard.app()

    elif menu=="AI Model":
        ai_model.app()

    elif menu=="Map":
        map.app()

    elif menu=="Report":
        report.app()

    elif menu=="Logout":
        st.session_state.logged_in=False
        st.rerun()