import streamlit as st

def app():
    st.title("📘 Tool Instructions")

    st.subheader("How to Use This Tool")
    st.markdown("""
    1. Navigate to the **Home** page.
    2. Enter the URL of the website you want to analyze.
    3. Click **Start Crawling** to begin the multilingual scan.
    4. After the process finishes, visit the **Reports** section to:
        - Download the Excel reports for each language.
        - Download ZIP files containing the raw HTML pages.
    5. Use the extracted files inside CAT tools like **Trados** or **memoQ**.

    **Notes:**
    - Only internal website pages are crawled.
    - External links (like social media) are skipped.
    - Media detection is included.
    """)

    st.subheader("🧑‍💼 Developer Information")
    st.markdown("""
    **Name**: Ahmed Mostafa Saad  
    **Position**: Localization Engineering & TMS Support Team Lead  
    **Email**: [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)  
    **Company**: Future Group Translation Services  
    """)
