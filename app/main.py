# app/main.py

import streamlit as st
import os
from pages import home, about

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_custom_css()

    # Header
    st.markdown("""
        <h1 style='text-align: center;'>🌍 Website Localization Scrapy Tool</h1>
        <p style='text-align: center; font-size: 16px;'>Your smart assistant for crawling, analyzing and preparing localization-ready website packages</p>
        <hr>
    """, unsafe_allow_html=True)

    # Page Router
    page = st.sidebar.radio("📌 Select Page", ["Home", "About"])

    if page == "Home":
        home.home_page()
    elif page == "About":
        about.about_page()


if __name__ == "__main__":
    main()
