import streamlit as st
import os
import pandas as pd
from io import BytesIO
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
from datetime import datetime

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def fetch_html_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Failed to fetch the page: {e}")
        return None

def analyze_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    words = text.split()
    return {
        "Word Count": len(words),
        "Title": soup.title.string if soup.title else "N/A",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

def save_html_as_zip(html_content, url):
    zip_io = BytesIO()
    with ZipFile(zip_io, 'w') as zip_file:
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".html"
        zip_file.writestr(filename, html_content)
    zip_io.seek(0)
    return zip_io

def main():
    st.set_page_config(page_title="Scrapy Localization Tool", layout="wide")
    load_custom_css()
    st.title("🌐 Website Scraping & Localization Estimator Tool")

    if 'results' not in st.session_state:
        st.session_state.results = None
        st.session_state.excel_data = None
        st.session_state.zip_data = None

    st.markdown("""
        **Instructions:**
        - Enter a full website URL to extract word/segment count and metadata.
        - Download Excel or HTML ZIP once analysis is complete.
    """)

    if st.button("🔄 Start New Session"):
        st.session_state.results = None
        st.session_state.excel_data = None
        st.session_state.zip_data = None
        st.experimental_rerun()

    if not st.session_state.results:
        url = st.text_input("🔗 Enter full website URL", placeholder="https://example.com")
        if st.button("🔍 Analyze Website") and url:
            with st.spinner("Fetching and analyzing..."):
                html = fetch_html_from_url(url)
                if html:
                    results = analyze_html(html)
                    df = pd.DataFrame([results])
                    st.session_state.results = df
                    st.session_state.excel_data = convert_df_to_excel(df)
                    st.session_state.zip_data = save_html_as_zip(html, url)
                    st.success(f"✅ Analysis complete for: {url}")

    if st.session_state.results is not None:
        st.dataframe(st.session_state.results)

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.download_button("📥 Download Excel Report", data=st.session_state.excel_data,
                               file_name="report.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col2:
            st.download_button("📦 Download HTML ZIP", data=st.session_state.zip_data,
                               file_name="html_page.zip", mime="application/zip")
        with col3:
            st.button("🔄 Start New Session")  # مكرر للتشجيع على الاستمرار

if __name__ == "__main__":
    main()
