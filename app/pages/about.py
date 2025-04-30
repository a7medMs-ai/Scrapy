# app/pages/about.py

import streamlit as st

def about_page():
    st.title("ℹ️ About Website Localization Scrapy Tool")

    st.markdown("### What is this tool?")
    st.write("""
    The Website Scrapy & Localization Tool is designed for localization professionals to automate the process of extracting website content, 
    performing pre-translation analysis, and generating structured reports (similar to CAT tools like Trados or memoQ).
    """)

    st.markdown("### Key Features")
    st.markdown("""
    - Crawl all public pages of any website.
    - Detect and classify by language automatically.
    - Generate Excel report with word count, segments, media presence.
    - Export HTML pages per language in ZIP format.
    """)

    st.markdown("### Technical Details")
    st.markdown("""
    - Built with Python, Streamlit, and aiohttp for asynchronous crawling.
    - Uses BeautifulSoup + langdetect for content and language analysis.
    - Generates Excel reports using openpyxl and pandas.
    """)

    st.markdown("### Developer Information")
    st.markdown("""
    **Ahmed Mostafa Saad**  
    🧑‍💼 *Localization Engineering & TMS Support Team Lead*  
    📧 [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)  
    🏢 Future Group Translation Services
    """)

    st.markdown("---")
    st.caption("Website Localization Engineering Tool © 2025 • v1.0.0")
