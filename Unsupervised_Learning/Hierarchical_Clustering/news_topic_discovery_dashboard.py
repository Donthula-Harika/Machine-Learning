# =========================================================
# 🟣 News Topic Discovery Dashboard
# Using Hierarchical Clustering
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# App Config
# ---------------------------------------------------------
st.set_page_config(page_title="News Topic Discovery Dashboard", layout="wide")

st.title("🟣 News Topic Discovery Dashboard")
st.markdown(
    "This system uses **Hierarchical Clustering** to automatically group similar "
    "news articles based on textual similarity."
)

# ---------------------------------------------------------
# Sidebar – Input Controls
# ---------------------------------------------------------
st.sidebar.header("📂 Dataset Handling")

uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

# Robust CSV loading
df = pd.read_csv(uploaded_file, encoding="latin1")

# Detect text column
text_columns = df.select_dtypes(include="object").columns.tolist()

text_col = st.sidebar.selectbox("Select Text Column", text_columns)

# ---------------------------------------------------------
# Text Vectorization Controls
# ---------------------------------------------------------
st.sidebar.header("📝 Text Vectorization")

max_features = st.sidebar.slider(
    "Maximum TF-IDF Features", 100, 2000, 1000
)

use_stopwords = st.sidebar.checkbox("Use English Stopwords", value=True)

ngram_option = st.sidebar.selectbox(
    "N-gram Range",
    ["Unigrams", "Bigrams", "Unigrams + Bigrams"]
)

ngram_map = {
    "Unigrams": (1, 1),
    "Bigrams": (2, 2),
    "Unigrams + Bigrams": (1, 2)
}

# ---------------------------------------------------------
# Hierarchical Clustering Controls
# ---------------------------------------------------------
st.sidebar.header("🌳 Hierarchical Clustering")

linkage_method = st.sidebar.selectbox(
    "Linkage Method", ["ward", "complete", "average", "single"]
)

distance_metric = "euclidean"

dendro_sample_size = st.sidebar.slider(
    "Number of Articles for Dendrogram", 20, 200, 50
)

# ---------------------------------------------------------
# TF-IDF Vectorization
# ---------------------------------------------------------
vectorizer = TfidfVectorizer(
    max_features=max_features,
    stop_words="english" if use_stopwords else None,
    ngram_range=ngram_map[ngram_option]
)

X = vectorizer.fit_transform(df[text_col].astype(str))

# ---------------------------------------------------------
# Dendrogram Section
# ---------------------------------------------------------
st.subheader("🌳 Hierarchical Dendrogram")

if st.button("🟦 Generate Dendrogram"):
    sample_X = X[:dendro_sample_size].toarray()

    Z = linkage(sample_X, method=linkage_method, metric=distance_metric)

    fig, ax = plt.subplots(figsize=(12, 5))
    dendrogram(Z, ax=ax)
    ax.set_title("Dendrogram (Subset of Articles)")
    ax.set_xlabel("Article Index")
    ax.set_ylabel("Distance")

    st.pyplot(fig)

# ---------------------------------------------------------
# Apply Clustering
# ---------------------------------------------------------
st.subheader("🟩 Apply Clustering")

n_clusters = st.slider("Select Number of Clusters", 2, 10, 3)

cluster_model = AgglomerativeClustering(
    n_clusters=n_clusters,
    linkage=linkage_method,
    metric=distance_metric
)

labels = cluster_model.fit_predict(X.toarray())
df["Cluster"] = labels

# ---------------------------------------------------------
# PCA Visualization
# ---------------------------------------------------------
st.subheader("📉 Cluster Visualization (PCA Projection)")

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X.toarray())

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=labels,
    cmap="tab10",
    alpha=0.7
)

ax.set_title("2D Projection of News Articles")
ax.set_xlabel("PCA Component 1")
ax.set_ylabel("PCA Component 2")

st.pyplot(fig)

# ---------------------------------------------------------
# Cluster Summary Section
# ---------------------------------------------------------
st.subheader("📊 Cluster Summary (Business View)")

feature_names = np.array(vectorizer.get_feature_names_out())

summary = []

for cluster_id in range(n_clusters):
    cluster_indices = np.where(labels == cluster_id)[0]
    cluster_size = len(cluster_indices)

    cluster_tfidf = X[cluster_indices].mean(axis=0)
    top_terms_idx = np.argsort(cluster_tfidf.A1)[::-1][:10]
    top_terms = ", ".join(feature_names[top_terms_idx])

    sample_text = df.loc[cluster_indices[0], text_col][:200]

    summary.append(
        {
            "Cluster ID": cluster_id,
            "Number of Articles": cluster_size,
            "Top Keywords": top_terms,
            "Sample Article Snippet": sample_text
        }
    )

summary_df = pd.DataFrame(summary)
st.dataframe(summary_df, use_container_width=True)

# ---------------------------------------------------------
# Validation Section
# ---------------------------------------------------------
st.subheader("📊 Clustering Validation")

sil_score = silhouette_score(X, labels)

st.metric("Silhouette Score", round(sil_score, 3))

st.caption(
    "Close to 1 → well-separated clusters | "
    "Close to 0 → overlapping clusters | "
    "Negative → poor clustering"
)

# ---------------------------------------------------------
# Business Interpretation Section
# ---------------------------------------------------------
st.subheader("🧠 Business Interpretation")

for row in summary:
    st.markdown(
        f"**🟣 Cluster {row['Cluster ID']}**: "
        f"Articles mainly focus on themes related to "
        f"{row['Top Keywords'].split(',')[0:3]}"
    )

# ---------------------------------------------------------
# User Guidance
# ---------------------------------------------------------
st.info(
    "Articles grouped in the same cluster share similar vocabulary and themes. "
    "These clusters can be used for automatic tagging, recommendations, "
    "and content organization."
)
