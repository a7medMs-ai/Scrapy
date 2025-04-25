import streamlit as st
from utils.excel_report_generator import generate_excel_report

def main():
    st.set_page_config(page_title="Excel Report Generator", layout="centered")
    st.title("📊 Excel Report Generator")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        df_original = generate_excel_report(uploaded_file)
        if df_original:
            st.success("✅ Excel report generated successfully.")
        else:
            st.error("❌ Failed to generate Excel report.")
    else:
        st.info("📁 Please upload an Excel file to proceed.")

if __name__ == "__main__":
    main()
