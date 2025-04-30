import streamlit as st
import os
from analyzer.content_analyzer import extract_page_data
from utils.excel_report_generator import generate_excel_report, get_excel_filename
import zipfile
import io

def app():
    st.title("🌐 Website Localization Analysis")

    st.markdown("### Upload HTML Files Organized by Language")
    st.markdown("Each language should be in a separate folder (e.g. 'ar', 'en').")

    uploaded_folder = st.file_uploader("Upload ZIP file of website pages", type=["zip"])

    if uploaded_folder:
        with zipfile.ZipFile(uploaded_folder, 'r') as zip_ref:
            extract_path = f"temp_data/{uploaded_folder.name.split('.')[0]}"
            zip_ref.extractall(extract_path)
            st.success("Files extracted successfully.")

            # Detect folders = languages
            languages = [f for f in os.listdir(extract_path) if os.path.isdir(os.path.join(extract_path, f))]
            data_by_language = {}

            for lang in languages:
                lang_path = os.path.join(extract_path, lang)
                st.markdown(f"Analyzing language: `{lang}` ...")
                page_data = []

                counter = 1
                for filename in sorted(os.listdir(lang_path)):
                    if filename.endswith(".html"):
                        file_path = os.path.join(lang_path, filename)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            html = f.read()
                        page_url = f"file://{filename}"
                        page_data.append(
                            extract_page_data(html, page_url, filename, counter)
                        )
                        counter += 1
                data_by_language[lang] = page_data

            # Generate Excel report
            st.markdown("### 📊 Download Excel Report")
            site_name = uploaded_folder.name.replace('.zip', '')
            excel_file = generate_excel_report(data_by_language, site_name)
            excel_name = get_excel_filename(site_name)
            st.download_button("📥 Download Excel", data=excel_file, file_name=excel_name)

            # Generate ZIP for each language
            st.markdown("### 🗂️ Download HTML ZIPs per Language")
            for lang in data_by_language:
                lang_zip_bytes = io.BytesIO()
                with zipfile.ZipFile(lang_zip_bytes, "w") as zf:
                    lang_folder_path = os.path.join(extract_path, lang)
                    for filename in os.listdir(lang_folder_path):
                        full_path = os.path.join(lang_folder_path, filename)
                        zf.write(full_path, arcname=filename)
                lang_zip_bytes.seek(0)
                st.download_button(
                    label=f"Download {lang.upper()} ZIP",
                    data=lang_zip_bytes,
                    file_name=f"{site_name}_{lang}.zip",
                    key=f"zip_{lang}"
                )
