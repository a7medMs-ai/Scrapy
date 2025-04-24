import streamlit as st
import os

def app():
    st.title("📊 التقارير والملفات")
    reports_dir = os.path.join("data", "reports")
    zips_dir = os.path.join("data", "zips")

    st.subheader("📄 تقارير Excel")
    if os.path.exists(reports_dir):
        for report_file in os.listdir(reports_dir):
            if report_file.endswith(".xlsx"):
                st.write(f"📄 {report_file}")
                with open(os.path.join(reports_dir, report_file), "rb") as f:
                    st.download_button(label="📥 تحميل التقرير", data=f, file_name=report_file)
    else:
        st.warning("لا توجد تقارير متاحة.")

    st.subheader("🗜️ ملفات ZIP")
    if os.path.exists(zips_dir):
        for zip_file in os.listdir(zips_dir):
            if zip_file.endswith(".zip"):
                st.write(f"🗜️ {zip_file}")
                with open(os.path.join(zips_dir, zip_file), "rb") as f:
                    st.download_button(label="📥 تحميل الملف", data=f, file_name=zip_file)
    else:
        st.warning("لا توجد ملفات ZIP متاحة.")
