import streamlit as st
import subprocess
import os
from pathlib import Path
from utils.zip_exporter import zip_html_pages
from utils.excel_report_generator import generate_excel_report

# Constants
HTML_PATH = "output/html_pages"
ZIP_PATH = "output/zips"

# Streamlit UI
st.set_page_config(page_title="Multilingual Website Crawler", layout="wide")
st.title("🌍 Multilingual Website Crawler")
st.caption("Developed by Localization Engineering Team")

# URL input
url = st.text_input("Enter website URL:", placeholder="https://example.com")

if st.button("Start Crawling"):
    if not url.strip():
        st.warning("Please enter a valid URL.")
    else:
        st.info("Crawling in progress... Please wait...")

        # Ensure output folders
        Path("output").mkdir(exist_ok=True)

        # Run Scrapy spider from crawler/ folder
        result = subprocess.run(
            ["scrapy", "crawl", "multilingual_spider", "-a", f"start_url={url}"],
            capture_output=True,
            text=True,
            cwd="crawler"  # <- Important: ensure you have the scrapy project here
        )

        # Error handling
        if result.returncode != 0:
            st.error("Crawling failed. Please check the logs.")
            st.code(result.stderr)
        else:
            st.success("✅ Crawling completed successfully.")

            # Generate Excel report
            st.info("Generating Excel report...")
            try:
                report_file = generate_excel_report(html_root=HTML_PATH, url=url)
                st.success("✅ Excel report generated.")
                st.download_button(
                    label="📥 Download Excel Report",
                    data=open(report_file, "rb"),
                    file_name=os.path.basename(report_file),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error("Failed to generate Excel report.")
                st.code(str(e))

            # ZIP HTML pages
            st.info("Zipping downloaded HTML pages...")
            try:
                zip_files = zip_html_pages(HTML_PATH, ZIP_PATH)
                st.success("✅ ZIP files created.")
                for zip_file in zip_files:
                    filename = os.path.basename(zip_file)
                    st.download_button(
                        label=f"📦 Download {filename}",
                        data=open(zip_file, "rb"),
                        file_name=filename,
                        mime="application/zip"
                    )
            except Exception as e:
                st.error("Failed to create ZIP files.")
                st.code(str(e))
