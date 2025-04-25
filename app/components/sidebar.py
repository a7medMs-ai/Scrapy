import streamlit as st

def sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("""
    - **Home**: Start crawling a website  
    - **Settings**: Configure crawl behavior *(coming soon)*  
    - **Reports**: Download reports and ZIPs  
    - **About**: Instructions and developer info
    """)
