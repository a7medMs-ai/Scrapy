import streamlit as st

def app():
    st.title("ℹ️ Scrapy Localization Tool")
    
    st.markdown("""
    ## 🔧 About the Tool
    This tool was built for **Localization Engineers** working in translation and website content analysis.
    
    It helps in:
    - Crawling websites and downloading their pages in HTML format.
    - Organizing pages by language in separate ZIP files.
    - Generating detailed Excel reports (word counts, segments, media presence, and more).
    - Preparing packages ready for CAT tools like **SDL Trados** and **memoQ**.

    ## 🛠️ Built With
    - **Python**
    - **Streamlit** for web interface
    - **Scrapy** for website crawling
    - **Pandas & Openpyxl** for Excel reporting

    ## 👨‍💻 Developer Info
    - **Developer**: Your Name Here
    - **Company**: Your Company
    - **Email**: your.email@company.com
    - **GitHub**: [Scrapy Project Repository](https://github.com/your-repo-link)

    Feel free to reach out for any bugs, suggestions, or collaboration.
    """)
