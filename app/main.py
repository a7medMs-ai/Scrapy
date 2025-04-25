import streamlit as st
import subprocess
import os
import json
import zipfile
import pandas as pd

# Create ZIP from jsonl
def create_zip():
    with zipfile.ZipFile("data/output.zip", "w") as zipf:
        zipf.write("data/output.jsonl", arcname="output.jsonl")

# Convert JSONL to Excel
def json_to_excel(jsonl_file, excel_file):
    records = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                continue
    df = pd.DataFrame(records)
    df.to_excel(excel_file, index=False)

# Streamlit config
st.set_page_config(
    layout="wide",
    page_title="Multilingual Website Crawler",
    page_icon="🌐"
)

# Title and description
st.title("🌐 Multilingual Website Crawler Tool")
st.markdown("Analyze and extract multilingual content from websites using Scrapy.")

# URL input
url = st.text_input("Enter the website URL you want to analyze", "https://example.com")

if st.button("Start Crawling"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        st.info("Starting the crawling process...")
        os.makedirs("data", exist_ok=True)

        result = subprocess.run(
            ["scrapy", "crawl", "multilingual_spider", "-a", f"start_url={url}"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            st.error("An error occurred during crawling.")
            with st.expander("🔍 View Error Log (stderr)"):
                st.code(result.stderr)
            with st.expander("📜 View Process Log (stdout)"):
                st.code(result.stdout)
        else:
            st.success("Crawling completed successfully.")

            jsonl_path = "data/output.jsonl"
            zip_path = "data/output.zip"
            excel_path = "data/output.xlsx"

            if os.path.exists(jsonl_path):
                create_zip()
                json_to_excel(jsonl_path, excel_path)

                with open(zip_path, "rb") as f:
                    st.download_button("📦 Download as ZIP", f, file_name="output.zip", mime="application/zip")

                with open(excel_path, "rb") as f:
                    st.download_button("📊 Download as Excel", f, file_name="output.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                with open(jsonl_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                parsed = [json.loads(line) for line in lines if line.strip()]
                with st.expander("📁 View Raw JSONL"):
                    st.json(parsed)
            else:
                st.warning("No output data found. Make sure the spider scraped something.")

# Footer - About
st.markdown("---")
st.subheader("ℹ️ About This Tool")
st.markdown("""
This tool crawls websites starting from a given URL, extracts multilingual content, and detects the language of each page.

**Features:**
- Language detection using `langdetect`
- HTML parsing using `BeautifulSoup`
- Structured export to `.jsonl`, `.xlsx`, and `.zip`
- User-friendly interface built with Streamlit

**How to Use:**
1. Enter a valid website URL.
2. Click **Start Crawling**.
3. Download the results in your preferred format.

> ⚠️ Please ensure the website allows crawling.
""")
