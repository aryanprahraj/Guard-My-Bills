import pdfplumber
import pandas as pd
from typing import IO

def extract_transactions_from_pdf(file: IO):
    import logging
    import traceback
    rows = []
    file_path = getattr(file, 'name', str(file))
    try:
        with pdfplumber.open(file) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                logging.info(f"[PDF] File: {file_path}, Page {i+1}, Tables found: {len(tables)}")
                for table in tables:
                    for row in table:
                        if any(row):  # skip empty or blank rows
                            rows.append(row)
    except Exception as e:
        logging.error(f"PDF parsing failed for file: {file_path}")
        logging.error(f"Exception: {e}")
        logging.error(traceback.format_exc())
        raise
    # If no rows, return empty DataFrame with standard columns
    standard_columns = [
        'date', 'time', 'amount', 'merchant', 'city', 'country', 'category',
    ]
    if not rows:
        return pd.DataFrame(columns=standard_columns)
    # If only one row, treat as header, no data
    if len(rows) == 1:
        return pd.DataFrame(columns=rows[0])
    # Use first row as header, rest as data
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df
