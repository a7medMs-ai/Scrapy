# app/pages/about.py

import streamlit as st

def about_page():
    st.title("ℹ️ About This Tool")

    st.markdown("""
    This tool was designed for localization engineers and project managers to simplify the quotation and word count process for website translation projects.

    ### 🧰 Key Features
    - Crawl public websites without login credentials.
    - Extract pages per language.
    - Generate Excel reports (similar to Trados).
    - Export HTML files ready for CAT tools.

    ### 👨‍💻 Developer
    - **Name:** A7medMS (Tool Owner)
    - **Email:** a7medms.localize@gmail.com
    - **GitHub:** [github.com/a7medms](https://github.com/a7medms)
    - **Company:** Torjoman / Freelance

    ### 📍 Inspired by:
    - [Scrapy](https://scrapy.org/)
    - [Alfaaz by @thecodrr](https://github.com/thecodrr/alfaaz)
    - [change-status.streamlit.app](https://change-status.streamlit.app/)
    """)

    st.image("https://scrapy.org/img/logo.png", width=120)
