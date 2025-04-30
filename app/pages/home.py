# app/pages/home.py

import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.crawler import process_site

st.set_page_config(page_title="Website Scrapy Tool", layout="wide")

def home_page():
    st.title("🌐 Website Scrapy & Localization Tool")

    url = st.text_input("🌐 Website URL", placeholder="https://example.com")

    if st.button("🚀 Start Full Website Analysis"):
        if not url:
            st.warning("Please enter a valid URL.")
        else:
            with st.spinner("Crawling and analyzing all languages and pages..."):
                # هنا لا نمرر lang_code أو max_pages — يتم التعامل معهم داخل الدالة
                excel_path, zip_path, session_dir = process_site(url)

                st.success("✅ All done!")
                st.info("Download your results below:")

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
