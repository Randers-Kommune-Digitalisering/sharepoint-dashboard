import streamlit as st
from page.sharepoint import get_sharepoint_overview

st.set_page_config(page_title="Sharepoint Dashboard", page_icon="assets/favicon.ico")

get_sharepoint_overview()
