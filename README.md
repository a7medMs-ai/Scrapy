# 🌍 Website Localization Scrapy Tool

A web-based solution for localization engineers to crawl websites, analyze their content, and generate Trados-style reports.

## 🚀 Features
- Crawl entire websites (public pages).
- Extract all HTML pages and analyze:
  - Word count
  - Segment count
  - Media presence
  - Language detection
  - Full content
- Generate Excel reports (1 sheet per language).
- Export HTML pages in language-specific ZIP files.
- Streamlit-based UI.

## 📦 How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/Scrapy.git
cd Scrapy
pip install -r requirements.txt
streamlit run app/main.py
