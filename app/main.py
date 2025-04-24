import streamlit as st
import subprocess
import os
from utils.word_counter import analyze_html_files
from utils.zip_creator import create_language_zips

def main():
    st.title("🕸️ أداة تحليل مواقع متعددة اللغات")

    start_url = st.text_input("أدخل رابط الموقع:", "")
    if st.button("ابدأ الزحف"):
        if start_url:
            with st.spinner("جاري الزحف إلى الموقع..."):
                subprocess.run(["python", "run.py", start_url])
            st.success("تم الانتهاء من الزحف وتحليل البيانات.")
        else:
            st.error("يرجى إدخال رابط الموقع.")

    if st.button("عرض التقارير"):
        reports_dir = os.path.join("data", "reports")
        if os.path.exists(reports_dir):
            for report_file in os.listdir(reports_dir):
                if report_file.endswith(".xlsx"):
                    st.write(f"📄 تقرير: {report_file}")
                    with open(os.path.join(reports_dir, report_file), "rb") as f:
                        st.download_button(label="📥 تحميل التقرير", data=f, file_name=report_file)
        else:
            st.warning("لا توجد تقارير متاحة.")

    if st.button("تحميل ملفات ZIP"):
        zips_dir = os.path.join("data", "zips")
        if os.path.exists(zips_dir):
            for zip_file in os.listdir(zips_dir):
                if zip_file.endswith(".zip"):
                    st.write(f"🗜️ ملف: {zip_file}")
                    with open(os.path.join(zips_dir, zip_file), "rb") as f:
                        st.download_button(label="📥 تحميل الملف", data=f, file_name=zip_file)
        else:
            st.warning("لا توجد ملفات ZIP متاحة.")

if __name__ == "__main__":
    main()
