# كتابة ملف main.py المعدل بالكامل متضمناً استدعاء excel_report_generator

final_main_code = """
import streamlit as st
import subprocess
import os
import pandas as pd
from utils.zip_exporter import zip_html_pages
from utils.excel_report_generator import generate_excel_report
from pathlib import Path

HTML_PATH = "output/html_pages"
ZIP_PATH = "output/zips"

st.set_page_config(page_title="Multilingual Website Crawler", layout="wide")
st.title("🌍 Multilingual Website Crawler")
st.caption("Developed by Localization Engineering Team")

url = st.text_input("Enter website URL:", placeholder="https://example.com")

if st.button("Start Crawling"):
    if not url.strip():
        st.warning("Please enter a valid URL.")
    else:
        st.info("Crawling in progress... Please wait.")
        Path("output").mkdir(exist_ok=True)

        result = subprocess.run(
            ["scrapy", "crawl", "multilingual_spider", "-a", f"start_url={url}"],
            capture_output=True,
            text=True,
            cwd="crawler"
        )

        if result.returncode != 0:
            st.error("Crawling failed. Please check the logs.")
            st.code(result.stderr)
        else:
            st.success("Crawling completed successfully.")

            st.info("Generating Excel report...")
            excel_report_path = generate_excel_report(html_root=HTML_PATH, url=url)
            st.success("Excel report is ready.")
            st.download_button(
                "Download Excel Report",
                open(excel_report_path, "rb"),
                file_name=os.path.basename(excel_report_path)
            )

            st.info("Creating ZIP files for HTML pages...")
            zip_files = zip_html_pages(HTML_PATH, ZIP_PATH)
            for zip_file in zip_files:
                filename = os.path.basename(zip_file)
                st.download_button(
                    f"Download ZIP ({filename})",
                    open(zip_file, "rb"),
                    file_name=filename
                )
"""

# حفظ الملف في app/main.py
main_py_path = "/mnt/data/scrapy_project/Scrapy-main/app/main.py"
with open(main_py_path, "w", encoding="utf-8") as f:
    f.write(final_main_code)

main_py_path
