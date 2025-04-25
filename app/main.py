import streamlit as st
import subprocess
import os
import pandas as pd
from utils.zip_exporter import zip_html_pages
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from pathlib import Path

HTML_PATH = "output/html_pages"
ZIP_PATH = "output/zips"
EXCEL_REPORT_PATH = "output/Website_Crawl_Report.xlsx"

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
            text=True
        )

        if result.returncode != 0:
            st.error("Crawling failed. Please check the logs.")
            st.code(result.stderr)
        else:
            st.success("Crawling completed.")

            report_data = []
            for lang in os.listdir(HTML_PATH):
                lang_path = os.path.join(HTML_PATH, lang)
                if os.path.isdir(lang_path):
                    for filename in os.listdir(lang_path):
                        if filename.endswith(".html"):
                            file_path = os.path.join(lang_path, filename)
                            with open(file_path, "r", encoding="utf-8") as f:
                                html_content = f.read()

                            soup = BeautifulSoup(html_content, "html.parser")
                            text = soup.get_text(separator=" ", strip=True)
                            word_count = len(re.findall(r"\\w+", text))
                            segments = len(soup.find_all(["p", "div", "li", "span"]))
                            has_media = bool(soup.find_all(["img", "video", "audio"]))
                            title = soup.title.string.strip() if soup.title else filename

                            report_data.append({
                                "Lang": lang,
                                "Page Counter": len(report_data) + 1,
                                "Page Name": filename,
                                "Title": title,
                                "Word Count": word_count,
                                "Segments": segments,
                                "Has Media": has_media,
                                "File Path": file_path
                            })

            df_report = pd.DataFrame(report_data)

            with pd.ExcelWriter(EXCEL_REPORT_PATH, engine="xlsxwriter") as writer:
                for lang in df_report["Lang"].unique():
                    df_lang = df_report[df_report["Lang"] == lang].drop(columns=["Lang"])
                    df_lang.to_excel(writer, sheet_name=lang[:31], index=False)

            st.success("Excel report generated.")
            st.download_button("Download Excel Report", open(EXCEL_REPORT_PATH, "rb"), file_name="Website_Crawl_Report.xlsx")

            zip_files = zip_html_pages(HTML_PATH, ZIP_PATH)
            for zip_file in zip_files:
                filename = os.path.basename(zip_file)
                st.download_button(f"Download ZIP ({filename})", open(zip_file, "rb"), file_name=filename)
