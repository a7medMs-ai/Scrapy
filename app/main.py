import streamlit as st
import subprocess
import os
import json
import zipfile
import pandas as pd

def create_zip():
    with zipfile.ZipFile("data/output.zip", "w") as zipf:
        zipf.write("data/output.json", arcname="output.json")

def json_to_excel(json_file, excel_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_excel(excel_file, index=False)

# Streamlit page config
st.set_page_config(
    layout="wide",
    page_title="Multilingual Website Crawler",
    page_icon="🌐"
)

st.title("🌐 Multilingual Website Crawler Tool")
st.markdown("Analyze and extract multilingual content from websites using Scrapy.")

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

            json_path = "data/output.json"
            zip_path = "data/output.zip"
            excel_path = "data/output.xlsx"

            if os.path.exists(json_path):
                create_zip()
                json_to_excel(json_path, excel_path)

                with open(zip_path, "rb") as f:
                    st.download_button("📦 Download as ZIP", f, file_name="output.zip", mime="application/zip")

                with open(excel_path, "rb") as f:
                    st.download_button("📊 Download as Excel", f, file_name="output.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                with open(json_path, "r", encoding="utf-8") as f:
                    raw_json = json.load(f)
                with st.expander("📁 View Raw JSON"):
                    st.json(raw_json)
            else:
                st.warning("No output data found. Make sure the spider scraped something.")
