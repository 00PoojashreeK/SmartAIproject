import streamlit as st
import auth
import dashboard
import upload
import ai_model
import map
import chatbot
import report

st.set_page_config(
    page_title="NGO Smart Resource Allocation",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Responsive styling for both light and dark modes */

:root {
    --primary-dark: #1b4332;
    --primary-medium: #2d6a4f;
    --primary-light: #40916c;
    --bg-light: #edf6f9;
    --bg-accent: #d8f3dc;
    --text-dark: #1b4332;
    --text-light: #555;
}

.stApp {
    background: linear-gradient(120deg, #edf6f9, #d8f3dc);
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .stApp {
        background: linear-gradient(120deg, #0f2818, #1b3d2f);
    }
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #1b4332;
    text-align: center;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #555;
}

.stButton>button {
    background: linear-gradient(90deg, #2d6a4f, #40916c);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #1b4332, #2d6a4f);
    transform: scale(1.02);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b4332, #2d6a4f) !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    text-align: center;
}

@media (prefers-color-scheme: dark) {
    .card {
        background: #1e1e1e;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.5);
        color: white;
    }
}

.login-box {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.15);
}

@media (prefers-color-scheme: dark) {
    .login-box {
        background: #2d2d2d;
        box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.5);
        color: white;
    }
}

</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOGIN PAGE ----------------

if not st.session_state.logged_in:

    st.markdown('<p class="main-title">🌍 NGO Smart Resource Allocation</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI Powered Disaster Management Platform</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,3,2])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        option = st.radio("", ["Login","Signup"])

        if option == "Login":
            auth.login()
        else:
            auth.register()

        st.markdown('</div>', unsafe_allow_html=True)


# ---------------- MAIN APP ----------------

else:

    auth.profile_sidebar()

    # -------- Sidebar Navigation --------

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    st.sidebar.markdown("""
    <style>

    .nav-btn{
        padding:10px;
        border-radius:8px;
        margin-bottom:5px;
    }

    .nav-active{
        background-color:#2d6a4f;
        color:white;
        font-weight:bold;
    }

    .nav-normal{
        background-color:#f1f1f1;
    }

    </style>
    """, unsafe_allow_html=True)


    def nav_button(name, icon):

        active = st.session_state.page == name

        if active:
            btn_class = "nav-active"
        else:
            btn_class = "nav-normal"

        if st.sidebar.button(f"{icon}  {name}", use_container_width=True):
            st.session_state.page = name


    nav_button("Dashboard","📊")
    nav_button("Upload Dataset","📂")
    nav_button("AI Model","🧠")
    nav_button("Map","🗺")
    nav_button("Chatbot","🤖")
    nav_button("Report","📄")

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


    menu = st.session_state.page


    if menu == "Dashboard":
        dashboard.app()

    elif menu == "Upload Dataset":
        upload.app()

    elif menu == "AI Model":
        ai_model.app()

    elif menu == "Map":
        map.app()

    elif menu == "Chatbot":
        chatbot.app()

    elif menu == "Report":
        report.app()