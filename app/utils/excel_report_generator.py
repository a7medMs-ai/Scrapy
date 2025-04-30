import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from io import BytesIO
import os

def generate_excel_report(data_by_language: dict, site_name: str) -> BytesIO:
    '''
    Generates a structured Excel report with one sheet per language.

    Parameters:
    - data_by_language (dict): Dictionary with language codes as keys and list of page data as values.
    - site_name (str): Website name to include in the Excel file name.

    Returns:
    - BytesIO: In-memory Excel file ready for download.
    '''

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')

    for language, pages in data_by_language.items():
        df = pd.DataFrame(pages)

        # Add total rows for Word Count and Segment Count
        if 'Word Count' in df.columns and 'Segments' in df.columns:
            total_row = {
                'Page Counter': 'TOTAL',
                'Word Count': df['Word Count'].sum(),
                'Segments': df['Segments'].sum()
            }
            df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

        df.to_excel(writer, sheet_name=language[:31], index=False)

        # Apply bold font to header row
        worksheet = writer.sheets[language[:31]]
        for cell in worksheet[1]:
            cell.font = Font(bold=True)

    writer.close()
    output.seek(0)
    return output

def get_excel_filename(site_name: str) -> str:
    '''
    Returns a proper Excel filename based on the site name.
    '''
    site_name_clean = site_name.replace('https://', '').replace('http://', '').split('/')[0].replace('.', '_')
    return f"website_{site_name_clean}_Scrapy.xlsx"
    
