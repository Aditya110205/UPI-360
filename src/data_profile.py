"""Profile raw UPI data to understand structure, types, and coverage."""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

data_dir = Path("data/raw")
files = sorted(data_dir.glob("*.xlsx"))

dfs = []
for file in files:
    df = pd.read_excel(file)
    df['source_file'] = file.name
    dfs.append(df)

# Combine all data
raw_df = pd.concat(dfs, ignore_index=True)

print("=" * 80)
print("DATA PROFILE: UPI Product Statistics")
print("=" * 80)
print(f"\nShape: {raw_df.shape[0]} rows × {raw_df.shape[1]} columns")
print(f"Date Range: {files[0].name} to {files[-1].name}")

print("\n--- COLUMNS & TYPES ---")
print(raw_df.dtypes)

print("\n--- FIRST FEW ROWS ---")
print(raw_df.head())

print("\n--- NULL VALUES ---")
nulls = raw_df.isnull().sum()
null_pct = (nulls / len(raw_df) * 100).round(1)
print(nulls[nulls > 0] if nulls.sum() > 0 else "No nulls found")
print(f"Total: {nulls.sum()} nulls across all cells")

print("\n--- DUPLICATES ---")
print(f"Complete duplicates: {raw_df.duplicated().sum()}")

print("\n--- UNIQUE VALUES (non-numeric) ---")
for col in raw_df.select_dtypes(include='object').columns:
    if col != 'source_file':
        print(f"{col}: {raw_df[col].nunique()} unique values")
        print(f"  Sample: {raw_df[col].unique()[:5]}")

print("\n--- NUMERIC STATS ---")
print(raw_df.describe())

print("\n--- FILE COVERAGE ---")
print(raw_df['source_file'].value_counts().sort_index())

print("\n" + "=" * 80)
