import pandas as pd
import streamlit as st

def generate_excel_report(uploaded_file):
    """
    Reads an uploaded Excel file and processes each sheet.

    Parameters:
    - uploaded_file: The uploaded Excel file from Streamlit's file uploader.

    Returns:
    - dict: A dictionary with sheet names as keys and DataFrames as values.
    """
    try:
        # Read all sheets into a dictionary
        df_original = pd.read_excel(uploaded_file, sheet_name=None)
    except Exception as e:
        st.error(f"An error occurred while reading the Excel file: {e}")
        return None

    # Process each sheet
    for sheet_name, df in df_original.items():
        st.write(f"Processing sheet: {sheet_name}, Rows: {len(df)}")
        # Add your processing logic here

    return df_original
