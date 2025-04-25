import os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def analyze_html_files(base_dir, base_url):
    reports = {}
    reports_dir = os.path.join("data", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    for lang in os.listdir(base_dir):
        lang_path = os.path.join(base_dir, lang)
        if not os.path.isdir(lang_path):
            continue

        records = []
        for file in os.listdir(lang_path):
            if not file.endswith(".html"):
                continue
            file_path = os.path.join(lang_path, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    text = soup.get_text(separator=" ", strip=True)

                    word_count = len(text.split())
                    segment_count = len(soup.find_all(["p", "div", "span"]))
                    has_media = bool(soup.find_all(["img", "audio", "video"]))

                    page_url = urljoin(base_url, file.replace("_", "/").replace(".html", ""))
                    
                    records.append({
                        "Page Name": file,
                        "Word Count": word_count,
                        "Segments": segment_count,
                        "Has Media": has_media,
                        "Page URL": page_url
                    })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        df = pd.DataFrame(records)
        output_path = os.path.join(reports_dir, f"{lang}_report.xlsx")
        df.to_excel(output_path, index=False)
        reports[lang] = output_path

    return reports
