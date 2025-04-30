import streamlit as st
import os
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
import subprocess
import uuid
import shutil

SCRAPY_OUTPUT_DIR = "output/html_pages"

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def run_scrapy_spider(start_url, output_folder):
    spider_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../crawler/spiders/multilingual_spider.py'))
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

    cmd = [
        "scrapy", "crawl", "multilingual",
        "-a", f"start_url={start_url}",
        "-s", f"FEED_URI={output_folder}/data.json",
        "-s", "FEED_FORMAT=json"
    ]

    subprocess.run(cmd, cwd=project_path, check=True)

def generate_excel_from_html(html_folder, url):
    data = []
    counter = 1
    for filename in os.listdir(html_folder):
        if filename.endswith(".html"):
            filepath = os.path.join(html_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()
                text = pd.read_html(filepath, flavor='bs4') if "<table" in html else None
                words = html.replace("<", " <").split()
                segments = html.count('<p>') + html.count('<div>') + html.count('<li>')
                has_media = any(ext in html for ext in ['.jpg', '.png', '.mp4', '.svg', '.webp'])
                data.append({
                    "Page Counter": counter,
                    "Page Name": filename.replace(".html", ""),
                    "Word Count": len(words),
                    "Segments": segments,
                    "Has Media": has_media,
                    "URL": url,
                    "Full Content": html[:3000],  # shortened for Excel
                    "Language": "en"
                })
                counter += 1

    df = pd.DataFrame(data)
    total_row = {
        "Page Counter": "TOTAL",
        "Page Name": None,
        "Word Count": df["Word Count"].sum(),
        "Segments": df["Segments"].sum(),
        "Has Media": None,
        "URL": None,
        "Full Content": None,
        "Language": None
    }
    df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    excel_buffer.seek(0)
    return df, excel_buffer

def zip_html_folder(folder_path):
    zip_io = BytesIO()
    with ZipFile(zip_io, "w") as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=arcname)
    zip_io.seek(0)
    return zip_io

def main():
    st.set_page_config(page_title="Scrapy Localization Tool", layout="wide")
    load_custom_css()
    st.title("🌐 Website Scraping & Localization Estimator Tool")

    if st.button("🔄 Start New Session", key="reset_button"):
        st.session_state.clear()
        st.experimental_rerun()

    if 'excel_data' not in st.session_state:
        url = st.text_input("🔗 Enter full website URL", placeholder="https://example.com")
        if st.button("🔍 Analyze Website"):
            unique_output = f"{SCRAPY_OUTPUT_DIR}_{uuid.uuid4().hex[:8]}"
            os.makedirs(unique_output, exist_ok=True)
            try:
                with st.spinner("Scraping website... This might take a moment."):
                    run_scrapy_spider(url, unique_output)
                    df, excel_data = generate_excel_from_html(unique_output, url)
                    zip_data = zip_html_folder(unique_output)

                    st.session_state.df = df
                    st.session_state.excel_data = excel_data
                    st.session_state.zip_data = zip_data
                    st.success(f"✅ Analysis complete for: {url}")
            except Exception as e:
                st.error(f"Scrapy spider failed: {e}")

    if 'df' in st.session_state:
        st.dataframe(st.session_state.df)

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.download_button("📥 Download Excel Report",
                               data=st.session_state.excel_data,
                               file_name="scrapy_report.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               key="excel_button")
        with col2:
            st.download_button("📦 Download HTML ZIP",
                               data=st.session_state.zip_data,
                               file_name="scraped_html_pages.zip",
                               mime="application/zip",
                               key="zip_button")
        with col3:
            st.button("🔄 Start New Session", key="start_again")

if __name__ == "__main__":
    main()
