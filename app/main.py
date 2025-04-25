import streamlit as st
import subprocess
import os

# UI Configuration
st.set_page_config(
    layout="wide",
    page_title="Multilingual Website Crawler",
    page_icon="🌐"
)

# Main Header
st.title("🌐 Multilingual Website Crawler Tool")
st.markdown("Analyze and extract multilingual content from websites using Scrapy.")

# Input section
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
            with st.expander("📜 View Output Log"):
                st.code(result.stdout)

# About / Instructions Section
st.markdown("---")
st.subheader("ℹ️ About This Tool")
st.markdown("""
This tool crawls websites starting from a given URL, extracts multilingual content, and detects the language of each page.

**Features:**
- Language detection using `langdetect`
- HTML parsing using `BeautifulSoup`
- Structured JSON export via Scrapy pipelines
- Easy-to-use interface powered by Streamlit

**How to Use:**
1. Enter the full URL of a website you'd like to crawl.
2. Click the **Start Crawling** button.
3. The crawler will extract text content and store it inside the `data/output.json` file.
4. View logs inside the expanders if something goes wrong.

> ⚠️ Make sure the target website allows crawling and does not block bots.
""")
