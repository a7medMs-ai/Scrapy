import os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def analyze_html_files(base_dir, base_url):
    reports = {}
    for lang in os.listdir(base_dir):
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.isdir(lang_dir):
            continue

        data = []
        for filename in os.listdir(lang_dir):
            if not filename.endswith('.html'):
                continue
            filepath = os.path.join(lang_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text()
                word_count = len(text.split())
                segment_count = len(soup.find_all(['p', 'div', 'span']))
                has_media = bool(soup.find_all(['img', 'video', 'audio']))
                page_url = urljoin(base_url, filename.replace('_', '/').replace('.html', ''))
                data.append({
                    'اسم الصفحة': filename,
                    'عدد الكلمات': word_count,
                    'عدد الفقرات': segment_count,
                    'تحتوي على وسائط': has_media,
                    'رابط الصفحة': page_url
                })

        df = pd.DataFrame(data)
        report_path = os.path.join('data', 'reports', f'{lang}_report.xlsx')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        df.to_excel(report_path, index=False)
        reports[lang] = report_path
    return reports
