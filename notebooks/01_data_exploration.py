import pandas as pd

# Load the dataset
file_path = "data/Online Retail.xlsx"

df = pd.read_excel(file_path)

# -----------------------------
# 1. First 5 rows
# -----------------------------
print("\n===== FIRST 5 ROWS =====")
print(df.head())

# -----------------------------
# 2. Number of rows and columns
# -----------------------------
print("\n===== DATASET SHAPE =====")
print(df.shape)

# -----------------------------
# 3. Column names
# -----------------------------
print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

# -----------------------------
# 4. Data types
# -----------------------------
print("\n===== DATA TYPES =====")
print(df.dtypes)

# -----------------------------
# 5. Missing values
# -----------------------------
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# -----------------------------
# 6. Duplicate rows
# -----------------------------
print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())