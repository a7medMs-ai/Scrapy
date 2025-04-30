import streamlit as st
import os
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
import subprocess
import uuid
import shutil
from urllib.parse import urlparse

SCRAPY_OUTPUT_ROOT = "output/html_pages"

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def run_scrapy_spider(start_url):
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    cmd = [
        "scrapy", "crawl", "multilingual_spider",
        "-a", f"start_url={start_url}",
    ]
    subprocess.run(cmd, cwd=project_path, check=True)

def generate_excel_from_scraped_html(base_dir, url):
    data = []
    counter = 1
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".html"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    html = f.read()
                    text = html.replace("<", " <").split()
                    segments = html.count('<p') + html.count('<div') + html.count('<li')
                    has_media = any(ext in html for ext in ['.jpg', '.png', '.mp4', '.svg', '.webp'])
                    data.append({
                        "Page Counter": counter,
                        "Page Name": filename.replace(".html", ""),
                        "Word Count": len(text),
                        "Segments": segments,
                        "Has Media": has_media,
                        "URL": url,
                        "Full Content": html[:3000],
                        "Language": os.path.basename(root)
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

    excel_io = BytesIO()
    with pd.ExcelWriter(excel_io, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    excel_io.seek(0)
    return df, excel_io

def zip_scrapy_output(base_dir):
    zip_io = BytesIO()
    with ZipFile(zip_io, "w") as zipf:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                path = os.path.join(root, file)
                arcname = os.path.relpath(path, base_dir)
                zipf.write(path, arcname)
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
        if st.button("🔍 Analyze Website") and url:
            domain = urlparse(url).netloc.replace("www.", "")
            try:
                with st.spinner("Scraping entire site (this may take a moment)..."):
                    shutil.rmtree(SCRAPY_OUTPUT_ROOT, ignore_errors=True)  # clean old output
                    run_scrapy_spider(url)
                    # get first subdir inside html_pages (e.g., 'en')
                    lang_dirs = [os.path.join(SCRAPY_OUTPUT_ROOT, d) for d in os.listdir(SCRAPY_OUTPUT_ROOT) if os.path.isdir(os.path.join(SCRAPY_OUTPUT_ROOT, d))]
                    if not lang_dirs:
                        raise Exception("No HTML pages found.")
                    df, excel_data = generate_excel_from_scraped_html(SCRAPY_OUTPUT_ROOT, url)
                    zip_data = zip_scrapy_output(SCRAPY_OUTPUT_ROOT)

                    st.session_state.df = df
                    st.session_state.excel_data = excel_data
                    st.session_state.zip_data = zip_data
                    st.session_state.domain = domain
                    st.success(f"✅ Analysis complete for: {url}")
            except Exception as e:
                st.error(f"Scrapy spider failed: {e}")

    if 'df' in st.session_state:
        st.dataframe(st.session_state.df)

        domain = st.session_state.domain or "website"
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.download_button("📥 Download Excel Report",
                               data=st.session_state.excel_data,
                               file_name=f"word-count_{domain}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               key="excel_button")
        with col2:
            st.download_button("📦 Download HTML ZIP",
                               data=st.session_state.zip_data,
                               file_name=f"HTML-Files_{domain}.zip",
                               mime="application/zip",
                               key="zip_button")
        with col3:
            st.button("🔄 Start New Session", key="start_again")

if __name__ == "__main__":
    main()
