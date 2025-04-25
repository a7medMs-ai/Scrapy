from urllib.parse import urlparse
import pandas as pd

def analyze_row(row):
    notes = []
    if row.get("Word Count", 0) == 0:
        notes.append("No visible text - possible rendering issue")
    if row.get("Segments", 0) < 5:
        notes.append("Very low structure - possible link-only page")
    if not row.get("Has Media", True):
        notes.append("No media found - text-only")
    return "; ".join(notes) if notes else ""

def generate_excel_report(df_original, base_url):
    parsed_url = urlparse(base_url)
    domain_name = parsed_url.netloc.replace("www.", "")
    log_filename = f"Log '{domain_name}'.xlsx"

    processed_sheets = {}

    for sheet, df in df_original.items():
        df = df.copy()

        # Remove "Title" column if it exists
        if "Title" in df.columns:
            df = df.drop(columns=["Title"])

        # Rename "File Path" to "URL" if it exists
        if "File Path" in df.columns:
            df = df.rename(columns={"File Path": "URL"})

        # Add "Notes" column based on analysis
        df["Notes"] = df.apply(analyze_row, axis=1)

        processed_sheets[sheet] = df

    # Write to Excel
    with pd.ExcelWriter(log_filename, engine='xlsxwriter') as writer:
        for sheet_name, df in processed_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return log_filename
