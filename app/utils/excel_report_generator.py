import os
import pandas as pd
import xlsxwriter
from urllib.parse import urlparse

def generate_excel_report(html_root):
    """
    Generate an Excel report from crawled HTML pages stored in the given html_root directory.

    Args:
        html_root (str): Path to the directory where HTML files are stored.

    Returns:
        str: Path to the generated Excel report.
    """
    # Build path to the CSV data extracted during crawling
    data_file_path = os.path.join(html_root, "extracted_data.csv")

    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"Data file not found: {data_file_path}")

    # Load the extracted data
    df = pd.read_csv(data_file_path)

    # Process and clean data
    df["Notes"] = df.apply(analyze_row, axis=1)

    # Parse domain name for naming
    domain_name = "website"
    try:
        parsed_url = urlparse(df['URL'].iloc[0])
        domain_name = parsed_url.netloc.replace("www.", "")
    except Exception:
        pass

    output_folder = os.path.join(html_root, "output")
    os.makedirs(output_folder, exist_ok=True)

    output_excel_path = os.path.join(output_folder, f"Log {domain_name}.xlsx")

    # Write to Excel
    with pd.ExcelWriter(output_excel_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Report", index=False)

    return output_excel_path

def analyze_row(row):
    """
    Analyze a row of extracted data to generate notes.

    Args:
        row (Series): A row of the dataframe.

    Returns:
        str: Notes based on content analysis.
    """
    notes = []

    if pd.isna(row.get("Word Count")) or row.get("Word Count", 0) == 0:
        notes.append("No visible text")
    
    if row.get("Segments", 0) < 5:
        notes.append("Low page structure")

    if not row.get("Has Media", True):
        notes.append("No media content")

    return "; ".join(notes) if notes else ""
