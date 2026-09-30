import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# ==========================================
# 1. Load customer RFM data
# ==========================================

df = pd.read_csv("data/customer_rfm.csv")

print("Customer dataset shape:", df.shape)


# ==========================================
# 2. Select features
# ==========================================

features = [
    "Recency",
    "Frequency",
    "Monetary"
]

X = df[features].copy()

# Reduce the effect of extreme values
X["Recency"] = X["Recency"].apply(lambda x: __import__("math").log1p(x))
X["Frequency"] = X["Frequency"].apply(lambda x: __import__("math").log1p(x))
X["Monetary"] = X["Monetary"].apply(lambda x: __import__("math").log1p(x))


# ==========================================
# 3. Scale the data
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\nData scaling completed.")


# ==========================================
# 4. Test different cluster numbers
# ==========================================

inertia = []
silhouette_scores = []

k_values = range(2, 11)

for k in k_values:

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X_scaled)

    inertia.append(kmeans.inertia_)

    score = silhouette_score(
        X_scaled,
        labels
    )

    silhouette_scores.append(score)


# ==========================================
# 5. Print scores
# ==========================================

print("\n===== SILHOUETTE SCORES =====")

for k, score in zip(k_values, silhouette_scores):

    print(
        f"K = {k} → Silhouette Score = {score:.4f}"
    )


# ==========================================
# 6. Choose final number of clusters
# ==========================================

final_k = 4

print("\nFinal number of clusters:", final_k)


# ==========================================
# 7. Train final KMeans model
# ==========================================

kmeans = KMeans(
    n_clusters=final_k,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X_scaled)


# ==========================================
# 8. Analyze customer segments
# ==========================================

cluster_summary = df.groupby("Cluster").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean")
).round(2)


print("\n===== CUSTOMER SEGMENT SUMMARY =====")

print(cluster_summary)


# ==========================================
# 9. Save segmented customer data
# ==========================================

df.to_csv(
    "data/customer_segments.csv",
    index=False
)

print("\nCustomer segmentation saved successfully!")


# ==========================================
# 10. Elbow Method
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    list(k_values),
    inertia,
    marker="o"
)

plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.xticks(list(k_values))

plt.tight_layout()

plt.savefig("images/elbow.png")

plt.show()


# ==========================================
# 11. Silhouette Score
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    list(k_values),
    silhouette_scores,
    marker="o"
)

plt.title("Silhouette Score by Number of Clusters")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.xticks(list(k_values))

plt.tight_layout()

plt.savefig("images/silhouette_scores.png")

plt.show()


print("\nClustering analysis completed successfully!")