import streamlit as st
from components import sidebar
from pages import home, about

# Inject custom CSS
def load_custom_css():
    with open("app/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_custom_css()
    sidebar.sidebar()

    page = st.sidebar.radio("Go to", ["Home", "About"])

    if page == "Home":
        home.app()
    elif page == "About":
        about.app()

if __name__ == "__main__":
    main()
