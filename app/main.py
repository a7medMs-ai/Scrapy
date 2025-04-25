import streamlit as st
import sys
import os

# Extend sys.path to allow importing from root and subfolders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import pages and components
from app.pages import home, settings, reports, about
from app.components.sidebar import sidebar
from app.components.header import header

def main():
    st.set_page_config(
        layout="wide",
        page_title="Multilingual Website Crawler",
        page_icon="🌍"
    )

    header()
    sidebar()

    # Sidebar navigation
    page = st.sidebar.radio("Navigate", ("Home", "Settings", "Reports", "About"))

    if page == "Home":
        home.app()
    elif page == "Settings":
        settings.app()
    elif page == "Reports":
        reports.app()
    elif page == "About":
        about.app()

if __name__ == "__main__":
    main()
