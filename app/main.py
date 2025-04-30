import streamlit as st
import os
from analyzer.html_processor import process_all_pages_parallel
import pandas as pd
from io import BytesIO

def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def analyze_html_folder(html_dir):
    return process_all_pages_parallel(html_dir)

@st.cache_data(show_spinner=False)
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

def main():
    st.set_page_config(page_title="Scrapy Localization Tool", layout="wide")
    load_custom_css()

    st.title("🌐 Website Scraping & Localization Estimator Tool")

    st.markdown("""
        **Instructions:**
        - Upload or select the folder containing HTML files.
        - Click 'Analyze Pages' to extract word/segment count and metadata.
        - Download Excel or ZIP files once analysis is complete.
    """)

    html_dir = st.text_input("📂 Enter path to HTML folder", "output/html_pages/ar")

    if st.button("🔍 Analyze Pages"):
        with st.spinner("Processing pages..."):
            results = analyze_html_folder(html_dir)
            if results:
                df = pd.DataFrame(results)
                excel_data = convert_df_to_excel(df)
                st.success(f"✅ Processed {len(results)} pages.")

                st.dataframe(df.head(100))  # عرض أول 100 صف فقط
                st.download_button(
                    "📥 Download Excel Report",
                    data=excel_data,
                    file_name="report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("⚠️ No HTML files found.")

if __name__ == "__main__":
    main()
