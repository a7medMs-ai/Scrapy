import streamlit as st

def sidebar():
    st.sidebar.title("📁 Navigation")
    st.sidebar.markdown("""
    - **Home**: Crawl and download website content  
    - **Reports**: View and download analysis reports  
    - **About**: Tool usage guide and developer info
    """)
