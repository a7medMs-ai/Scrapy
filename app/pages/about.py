import streamlit as st

def app():
    st.title("📘 Tool Instructions")

    st.subheader("How to Use This Tool")
    st.markdown("""
    1. Go to the **Home** page and enter a website URL.
    2. Click the **Start Crawling** button.
    3. The tool will automatically:
        - Crawl all internal pages.
        - Group them by language.
        - Extract content for localization analysis.
    4. Go to the **Reports** page to download:
        - Excel reports per language.
        - ZIP files for translation or CAT tools.
    """)

    st.subheader("🧑‍💼 Developer Information")
    st.markdown("""
    **Name**: Ahmed Mostafa Saad  
    **Position**: Localization Engineering & TMS Support Team Lead  
    **Email**: [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)  
    **Company**: Future Group Translation Services  
    """)
