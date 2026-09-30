import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# ==========================================
# 1. Load segmented customer data
# ==========================================

df = pd.read_csv("data/customer_segments.csv")

print("Dataset shape:", df.shape)


# ==========================================
# 2. Select RFM features
# ==========================================

features = [
    "Recency",
    "Frequency",
    "Monetary"
]

X = df[features].copy()


# ==========================================
# 3. Apply log transformation
# ==========================================

import numpy as np

X["Recency"] = np.log1p(X["Recency"])
X["Frequency"] = np.log1p(X["Frequency"])
X["Monetary"] = np.log1p(X["Monetary"])


# ==========================================
# 4. Standardize the data
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ==========================================
# 5. Apply PCA
# ==========================================

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)


# ==========================================
# 6. Add PCA columns
# ==========================================

df["PC1"] = X_pca[:, 0]
df["PC2"] = X_pca[:, 1]
# Save PCA results
df.to_csv(
    "data/customer_segments.csv",
    index=False
)

print("\nPCA results saved successfully!")

# ==========================================
# 7. Print explained variance
# ==========================================

print("\n===== PCA EXPLAINED VARIANCE =====")

print(
    "PC1:",
    round(pca.explained_variance_ratio_[0] * 100, 2),
    "%"
)

print(
    "PC2:",
    round(pca.explained_variance_ratio_[1] * 100, 2),
    "%"
)

print(
    "Total:",
    round(pca.explained_variance_ratio_.sum() * 100, 2),
    "%"
)


# ==========================================
# 8. Create PCA visualization
# ==========================================

plt.figure(figsize=(10, 7))

for cluster in sorted(df["Cluster"].unique()):

    cluster_data = df[df["Cluster"] == cluster]

    plt.scatter(
        cluster_data["PC1"],
        cluster_data["PC2"],
        label=f"Cluster {cluster}",
        alpha=0.6
    )


plt.title("Customer Segments - PCA Visualization")

plt.xlabel("Principal Component 1")

plt.ylabel("Principal Component 2")

plt.legend()

plt.tight_layout()

plt.savefig(
    "images/customer_segments_pca.png"
)

plt.show()


print("\nPCA visualization completed successfully!")