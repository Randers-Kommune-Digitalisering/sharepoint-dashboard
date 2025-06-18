import streamlit as st
from streamlit_option_menu import option_menu
from utils.logo import get_logo
from page.sharepoint import get_sharepoint_overview

st.set_page_config(page_title="Sharepoint Dashboard", page_icon="assets/favicon.ico")

with st.sidebar:
    st.sidebar.markdown(get_logo(), unsafe_allow_html=True)
    selected = option_menu(
        "Sharepoint Dashboard",
        ["Handleplan - T&D strategi"],
        default_index=0,
        icons=['bi bi-card-list'],
        menu_icon="bi bi-person-lines-fill",
        styles={
            "container": {"padding": "5px", "background-color": "#f0f0f0"},
            "icon": {"color": "#4a4a4a", "font-size": "18px"},
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "--hover-color": "#e0e0e0"},
            "nav-link-selected": {"background-color": "#d0d0d0", "color": "#4a4a4a"},
            "menu-title": {"font-size": "20px", "font-weight": "bold", "color": "#4a4a4a", "margin-bottom": "10px"},
        }
    )

if selected == "Handleplan - T&D strategi":
    get_sharepoint_overview()
