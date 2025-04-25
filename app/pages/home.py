import streamlit as st
import subprocess
import os

st.title("Multilingual Website Crawler Tool")

url = st.text_input("Enter the website URL you want to analyze", "https://example.com")

if st.button("Start Crawling"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        st.info("Starting the crawling process...")

        # Ensure output folder exists
        os.makedirs("data", exist_ok=True)

        # Run the spider and capture output and error logs
        result = subprocess.run(
            ["scrapy", "crawl", "multilingual_spider", "-a", f"start_url={url}"],
            capture_output=True,
            text=True
        )

        # Display logs based on result
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
