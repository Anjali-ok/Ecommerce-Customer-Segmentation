import pandas as pd

# ==========================================
# 1. Load the original dataset
# ==========================================

file_path = "data/Online Retail.xlsx"

df = pd.read_excel(file_path)

print("Original dataset shape:", df.shape)


# ==========================================
# 2. Remove duplicate rows
# ==========================================

df = df.drop_duplicates()

print("After removing duplicates:", df.shape)


# ==========================================
# 3. Remove rows without CustomerID
# ==========================================

df = df.dropna(subset=["CustomerID"])

print("After removing missing CustomerID:", df.shape)


# ==========================================
# 4. Remove cancelled transactions
# ==========================================

# In this dataset, InvoiceNo starting with "C"
# represents a cancelled transaction.

df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

print("After removing cancelled transactions:", df.shape)


# ==========================================
# 5. Remove invalid quantities
# ==========================================

df = df[df["Quantity"] > 0]

print("After removing invalid quantities:", df.shape)


# ==========================================
# 6. Remove invalid prices
# ==========================================

df = df[df["UnitPrice"] > 0]

print("After removing invalid prices:", df.shape)


# ==========================================
# 7. Create TotalAmount
# ==========================================

df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]


# ==========================================
# 8. Save cleaned dataset
# ==========================================

df.to_csv("data/cleaned_online_retail.csv", index=False)

print("\nCleaning completed successfully!")
print("Final dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())