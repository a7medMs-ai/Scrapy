import os
import zipfile

def create_language_zips(base_dir):
    zip_paths = []
    for lang in os.listdir(base_dir):
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.isdir(lang_dir):
            continue
        zip_path = os.path.join('data', 'zips', f'{lang}_pages.zip')
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(lang_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, lang_dir)
                    zipf.write(file_path, arcname)
        zip_paths.append(zip_path)

    # إنشاء ملف ZIP رئيسي يحتوي على جميع ملفات ZIP لكل لغة
    all_languages_zip = os.path.join('data', 'zips', 'all_languages.zip')
    with zipfile.ZipFile(all_languages_zip, 'w') as zipf:
        for zip_path in zip_paths:
            arcname = os.path.basename(zip_path)
            zipf.write(zip_path, arcname)
    return zip_paths, all_languages_zip
