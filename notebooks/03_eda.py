import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. Load cleaned data
# ==========================================

df = pd.read_csv("data/cleaned_online_retail.csv")

# Convert InvoiceDate back to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("Dataset shape:", df.shape)


# ==========================================
# 2. Basic business metrics
# ==========================================

total_revenue = df["TotalAmount"].sum()
total_customers = df["CustomerID"].nunique()
total_orders = df["InvoiceNo"].nunique()
total_products = df["StockCode"].nunique()

print("\n===== BUSINESS METRICS =====")
print("Total Revenue:", round(total_revenue, 2))
print("Total Customers:", total_customers)
print("Total Orders:", total_orders)
print("Total Products:", total_products)


# ==========================================
# 3. Top 10 countries by revenue
# ==========================================

country_revenue = (
    df.groupby("Country")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 COUNTRIES BY REVENUE =====")
print(country_revenue)


# ==========================================
# 4. Top 10 products by revenue
# ==========================================

product_revenue = (
    df.groupby("Description")["TotalAmount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 PRODUCTS BY REVENUE =====")
print(product_revenue)


# ==========================================
# 5. Revenue by month
# ==========================================

df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

monthly_revenue = (
    df.groupby("Month")["TotalAmount"]
    .sum()
)

print("\n===== MONTHLY REVENUE =====")
print(monthly_revenue)


# ==========================================
# 6. Revenue chart
# ==========================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("images/monthly_revenue.png")

plt.show()


# ==========================================
# 7. Top countries chart
# ==========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    x=country_revenue.values,
    y=country_revenue.index
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig("images/top_countries.png")

plt.show()