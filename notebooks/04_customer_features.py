import pandas as pd

# ==========================================
# 1. Load cleaned data
# ==========================================

df = pd.read_csv("data/cleaned_online_retail.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("Dataset shape:", df.shape)


# ==========================================
# 2. Find the last purchase date
# ==========================================

max_date = df["InvoiceDate"].max()

print("\nLast transaction date:", max_date)


# ==========================================
# 3. Create customer-level RFM features
# ==========================================

customer_data = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x:
             (max_date - x.max()).days),

    Frequency=("InvoiceNo", "nunique"),

    Monetary=("TotalAmount", "sum")
).reset_index()


# ==========================================
# 4. Display customer data
# ==========================================

print("\n===== CUSTOMER RFM DATA =====")

print(customer_data.head())


# ==========================================
# 5. Basic statistics
# ==========================================

print("\n===== RFM STATISTICS =====")

print(customer_data[[
    "Recency",
    "Frequency",
    "Monetary"
]].describe())


# ==========================================
# 6. Save customer-level dataset
# ==========================================

customer_data.to_csv(
    "data/customer_rfm.csv",
    index=False
)

print("\nCustomer RFM dataset saved successfully!")

print("Number of customers:",
      customer_data.shape[0])
