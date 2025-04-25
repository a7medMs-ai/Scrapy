import os
import pandas as pd
from urllib.parse import urlparse

def analyze_row(row):
    notes = []
    if row.get("Word Count", 0) == 0:
        notes.append("No visible text - possible rendering issue")
    if row.get("Segments", 0) < 5:
        notes.append("Very low structure - possible link-only page")
    if not row.get("Has Media", True):
        notes.append("No media found - text-only")
    return "; ".join(notes) if notes else ""

def generate_excel_report(html_root):
    """
    Generates an Excel report from crawled HTML data.

    Parameters:
    - html_root (str): The root directory where the HTML pages are stored.

    Returns:
    - str: The path to the generated Excel report.
    """
    # Ensure the output directory exists
    output_dir = os.path.join(html_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Define the path to the Excel report
    parsed_url = urlparse(html_root)
    domain_name = parsed_url.netloc.replace("www.", "")
    log_filename = f"Log_{domain_name}.xlsx"
    log_filepath = os.path.join(output_dir, log_filename)

    # Load the crawled data
    data_file = os.path.join(html_root, "crawled_data.json")
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Crawled data not found at {data_file}")

    with open(data_file, "r", encoding="utf-8") as f:
        crawled_data = pd.read_json(f)

    # Process the data
    crawled_data["Notes"] = crawled_data.apply(analyze_row, axis=1)

    # Save to Excel
    with pd.ExcelWriter(log_filepath, engine="xlsxwriter") as writer:
        crawled_data.to_excel(writer, index=False, sheet_name="Crawled Data")

    return log_filepath
