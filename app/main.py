import shutil
import zipfile

# تعديل محتوى main.py كما طلبنا بإزالة prefix "app."
final_main_py_content = """
import streamlit as st
from components import sidebar
from pages import home, about

# Inject custom CSS
def load_custom_css():
    with open("assets/style.css") as f:
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
"""

# مسار المشروع المراد تعديله وتجهيزه للتحميل
fixed_project_path = "/mnt/data/FixedScrapyApp"
source_path = "/mnt/data/ScrapyReview/Scrapy-main"

# نسخ المشروع بالكامل إلى مجلد جديد
shutil.copytree(source_path, fixed_project_path, dirs_exist_ok=True)

# الكتابة إلى main.py المعدل
main_py_path = os.path.join(fixed_project_path, "app", "main.py")
with open(main_py_path, "w", encoding="utf-8") as f:
    f.write(final_main_py_content)

# ضغط المشروع في ملف ZIP
zip_output_path = "/mnt/data/Scrapy_Localization_Tool_Final.zip"
with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(fixed_project_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, fixed_project_path)
            zipf.write(file_path, arcname=arcname)

zip_output_path
