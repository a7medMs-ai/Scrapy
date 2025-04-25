# إعادة كتابة محتوى ملف zip_exporter.py الذي يحتوي على الدالة zip_html_pages
zip_exporter_code = """
import os
import zipfile

def zip_html_pages(html_base_path, zip_output_root):
    '''
    Create ZIP archives for each language's HTML pages.

    Parameters:
    - html_base_path (str): Directory where folders like 'en', 'fr' exist.
    - zip_output_root (str): Output directory to save ZIP files.

    Returns:
    - list of str: Paths to created ZIP files.
    '''
    os.makedirs(zip_output_root, exist_ok=True)
    zip_files_created = []

    for lang in os.listdir(html_base_path):
        lang_dir = os.path.join(html_base_path, lang)
        if os.path.isdir(lang_dir):
            zip_path = os.path.join(zip_output_root, f"{lang}_html_pages.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(lang_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=lang_dir)
                        zipf.write(file_path, arcname=os.path.join(lang, arcname))
            zip_files_created.append(zip_path)

    return zip_files_created
"""

# تحديد المسار الصحيح للملف داخل app/utils/
zip_exporter_path = "/mnt/data/scrapy_project/Scrapy-main/app/utils/zip_exporter.py"
os.makedirs(os.path.dirname(zip_exporter_path), exist_ok=True)

with open(zip_exporter_path, "w", encoding="utf-8") as f:
    f.write(zip_exporter_code)

zip_exporter_path
