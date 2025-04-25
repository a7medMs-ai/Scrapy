import streamlit as st
import subprocess
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.word_counter import analyze_html_files
from utils.zip_creator import create_language_zips

def app():
    st.title("🏠 Home")
    st.subheader("Start Crawling a Website")

    start_url = st.text_input("Enter the website URL you want to analyze")

    if st.button("Start Crawling"):
        if not start_url:
            st.error("Please enter a valid URL.")
            return

        with st.spinner("Crawling in progress... this may take a few moments."):
            result = subprocess.run(["python", "run.py", start_url])

            if result.returncode == 0:
                st.success("Website crawl completed successfully.")
                st.info("Now generating reports and ZIP files...")
                analyze_html_files("data/raw", start_url)
                create_language_zips("data/raw")
                st.success("Reports and ZIPs generated successfully.")
            else:
                st.error("An error occurred during crawling. Please check logs.")
