# backend/report_generator.py

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
import os
import re

def clean_illegal_chars(text):
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", str(text))

def generate_excel_report(data_per_lang: dict, report_path: str):
    with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
        for lang_code, data in data_per_lang.items():
            cleaned_data = []
            for row in data:
                cleaned_row = {k: clean_illegal_chars(v) for k, v in row.items()}
                cleaned_data.append(cleaned_row)

            df = pd.DataFrame(cleaned_data)

            # إجماليات
            totals = {
                "Page Counter": "TOTAL",
                "Word Count": df["Word Count"].sum(),
                "Segments": df["Segments"].sum()
            }
            df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

            df.to_excel(writer, sheet_name=lang_code[:31], index=False)  # Excel limit: 31 chars

            # تنسيق TOTAL
            sheet = writer.book[lang_code[:31]]
            last_row = sheet.max_row
            for col in range(1, sheet.max_column + 1):
                cell = sheet.cell(row=last_row, column=col)
                if cell.value == "TOTAL":
                    cell.font = Font(bold=True, color="FF0000")
