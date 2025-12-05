"""
This script loads a messy sales dataset and applies several cleaning steps.
It standardizes column names, trims whitespace, handles missing values,
converts numeric fields, removes invalid rows, and outputs a cleaned CSV.
"""

import pandas as pd

# Function: Load the raw sales CSV file into a pandas DataFrame.
def load_data(file_path: str):
    df = pd.read_csv(file_path)
    return df

# Function: Standardize column names (lowercase, strip spaces, replace spaces with underscores).
def clean_column_names(df):
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )
    return df

# Function: Convert price + quantity columns to numeric
# Reason: Some values are messy (e.g., "$10", " 5 ", "??") and must be coerced to numbers.
def convert_numeric(df, price_col, quantity_col):
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df[quantity_col] = pd.to_numeric(df[quantity_col], errors="coerce")
    return df

# Function: Handle missing values in price and quantity.
def handle_missing_values(df, price_col, quantity_col):
    cleaned = df.dropna(subset=[price_col, quantity_col])
    return cleaned

# Function: Remove rows with negative price or quantity.
def remove_invalid_rows(df, price_col, quantity_col):
    df = df[df[price_col] >= 0]
    df = df[df[quantity_col] >= 0]
    return df

if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)

    print("Column names BEFORE cleaning:")
    print(df_raw.columns)

    # Step 1: Clean column names
    df_clean = clean_column_names(df_raw)

    # Your column names after cleaning:
    price_col = "price"
    quantity_col = "qty"

    # Step 2: Convert numeric fields
    df_clean = convert_numeric(df_clean, price_col, quantity_col)

    # Step 3: Drop missing numeric values
    df_clean = handle_missing_values(df_clean, price_col, quantity_col)

    # Step 4: Remove invalid (negative) values
    df_clean = remove_invalid_rows(df_clean, price_col, quantity_col)

    # Save cleaned CSV
    df_clean.to_csv(cleaned_path, index=False)

    print("\nCleaning complete. First few rows:")
    print(df_clean.head())



