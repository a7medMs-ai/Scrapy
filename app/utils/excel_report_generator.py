from urllib.parse import urlparse
import re
import os

# We'll simulate the URL for naming the file (normally this comes from the Streamlit input)
test_url = "https://torjoman.com"
parsed_url = urlparse(test_url)
domain_name = parsed_url.netloc.replace("www.", "")
log_filename = f"Log '{domain_name}'.xlsx"

# Function to estimate notes
def analyze_row(row):
    notes = []
    if row["Word Count"] == 0:
        notes.append("No visible text - possible rendering issue")
    if row["Segments"] < 5:
        notes.append("Very low structure - possible link-only page")
    if not row["Has Media"]:
        notes.append("No media found - text-only")
    return "; ".join(notes) if notes else ""

# Process each sheet and apply the transformations
processed_sheets = {}
for sheet, df in df_original.items():
    df = df.copy()
    # Remove "Title"
    if "Title" in df.columns:
        df = df.drop(columns=["Title"])
    # Rename File Path to URL
    df = df.rename(columns={"File Path": "URL"})
    # Add Notes column
    df["Notes"] = df.apply(analyze_row, axis=1)
    # Fix Word Count if needed (attempt to recalculate)
    if df["Word Count"].sum() == 0:
        def recount_words(url_path):
            try:
                with open(url_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                text = BeautifulSoup(html, "html.parser").get_text(separator=" ", strip=True)
                return len(re.findall(r"\\w+", text))
            except:
                return 0
        df["Word Count"] = df["URL"].apply(recount_words)

    processed_sheets[sheet] = df

# Save the cleaned report
final_excel_path = f"/mnt/data/{log_filename}"
with pd.ExcelWriter(final_excel_path, engine="xlsxwriter") as writer:
    for sheet, df in processed_sheets.items():
        df.to_excel(writer, sheet_name=sheet[:31], index=False)

final_excel_path
