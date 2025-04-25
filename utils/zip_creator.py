import os
import zipfile

def create_language_zips(base_dir):
    zip_output_dir = os.path.join("data", "zips")
    os.makedirs(zip_output_dir, exist_ok=True)

    language_zips = []

    for lang in os.listdir(base_dir):
        lang_path = os.path.join(base_dir, lang)
        if not os.path.isdir(lang_path):
            continue

        zip_path = os.path.join(zip_output_dir, f"{lang}_pages.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(lang_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, lang_path)
                    zipf.write(full_path, arcname)
        language_zips.append(zip_path)

    # Create master ZIP file containing all language zips
    master_zip = os.path.join(zip_output_dir, "all_languages.zip")
    with zipfile.ZipFile(master_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for zip_path in language_zips:
            arcname = os.path.basename(zip_path)
            zipf.write(zip_path, arcname)

    return language_zips, master_zip
