import pandas as pd
import os

def generate_excel_report(excel_file_path):
    """
    Reads an Excel file and processes each sheet.

    Parameters:
    - excel_file_path (str): Path to the Excel file.

    Returns:
    - dict: A dictionary with sheet names as keys and DataFrames as values.
    """
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"The file {excel_file_path} does not exist.")

    try:
        # Load all sheets into a dictionary
        df_original = pd.read_excel(excel_file_path, sheet_name=None)
    except Exception as e:
        raise ValueError(f"An error occurred while reading the Excel file: {e}")

    # Process each sheet
    for sheet_name, df in df_original.items():
        # Example processing: print sheet name and number of rows
        print(f"Processing sheet: {sheet_name}, Rows: {len(df)}")
        # Add your processing logic here

    return df_original
