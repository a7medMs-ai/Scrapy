import streamlit as st
import os
from analyzer.html_processor import process_all_pages_parallel
import pandas as pd

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Scrapy Localization Tool", layout="wide")
    load_custom_css()

    st.title("🌐 Website Scraping & Localization Estimator Tool")

    st.markdown(\"""
        **Instructions:**
        - Upload or select the folder containing HTML files.
        - Click 'Analyze Pages' to extract word/segment count and metadata.
        - Download Excel or ZIP files once analysis is complete.
    \""")

    html_dir = st.text_input("📂 Enter path to HTML folder", "output/html_pages/ar")

    if st.button("🔍 Analyze Pages"):
        with st.spinner("Processing pages..."):
            results = process_all_pages_parallel(html_dir)
            if results:
                df = pd.DataFrame(results)
                st.success(f"✅ Processed {len(results)} pages.")
                st.dataframe(df)
                # Optional: Export buttons
                if st.download_button("📥 Download Excel Report", data=df.to_excel(index=False), file_name="report.xlsx"):
                    st.success("Excel downloaded.")
            else:
                st.warning("⚠️ No HTML files found.")

    st.markdown("---")
    st.markdown("Developed by [Your Name] · For internal localization teams")

if __name__ == "__main__":
    main()
