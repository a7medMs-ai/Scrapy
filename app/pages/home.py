# app/pages/home.py

import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.crawler import process_site 

st.set_page_config(page_title="Website Scrapy Tool", layout="wide")

def home_page():
    st.title("🌐 Website Scrapy & Localization Tool")

    with st.expander("📝 Instructions", expanded=True):
        st.markdown("""
        1. Paste the website URL you want to analyze.
        2. Choose the language code (e.g., `ar`, `en`).
        3. Click **Start Crawling**.
        4. Download the Excel and ZIP once the process is complete.

        **Note:** Each session creates separate files. No overlap between runs.
        """)

    st.markdown("---")
    url = st.text_input("🔗 Enter the website URL (e.g., https://torjoman.com)")
    lang_code = st.text_input("🌍 Language Code (e.g., ar, en)", value="ar")
    max_pages = st.slider("📄 Max Pages to Crawl", 5, 100, 20)

    if st.button("🚀 Start Crawling and Analysis"):
        if not url or not lang_code:
            st.warning("Please enter both URL and language code.")
        else:
            with st.spinner("Crawling and analyzing... Please wait."):
                excel_path, zip_path, session_dir = process_site(url, lang_code=lang_code, max_pages=max_pages)

                st.success("✅ Done!")
                st.info("You can now download your results:")

                # Download buttons
                with open(excel_path, "rb") as f:
                    st.download_button(
                        label="📊 Download Excel Report",
                        data=f,
                        file_name=os.path.basename(excel_path),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="📁 Download HTML ZIP",
                        data=f,
                        file_name=os.path.basename(zip_path),
                        mime="application/zip"
                    )
