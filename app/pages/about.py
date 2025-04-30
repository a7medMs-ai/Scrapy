import streamlit as st

def about():
    st.title("About Scrapy Localization Tool")

    st.markdown("""
    ## What is this tool?

    The **Scrapy Localization Tool** helps you estimate translation efforts by scraping any live webpage,
    extracting text content and providing structured reports – all in seconds.

    ---

    ## Key Features

    - 🔗 Scrape any website via direct URL input
    - 📊 Count words, extract titles and timestamps
    - 📁 Download content as Excel or HTML ZIP
    - 🔁 Stay on the page for continuous analysis with “Start New Session”

    ---

    ## Technical Highlights

    - Built with **Python**, **Streamlit**, **BeautifulSoup**, **Pandas**
    - Instant download via memory (no files saved to disk)
    - Fast response using `st.session_state` to persist data

    ---

    ## Developer Info

    **Ahmed Mostafa Saad**  
    Team Lead – Localization Engineering  
    📧 [ahmed.mostafaa@future-group.com](mailto:ahmed.mostafaa@future-group.com)

    ---

    ## Need Support?

    If you have questions, feature ideas, or collaboration opportunities, don’t hesitate to reach out!
    """)

if __name__ == "__main__":
    about()
