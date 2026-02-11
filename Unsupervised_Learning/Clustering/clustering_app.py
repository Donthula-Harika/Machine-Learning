import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Customer Segmentation", layout="wide")

st.title("🧩 Wholesale Customer Segmentation")
st.caption("Behavior-based clustering for smarter business decisions")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("./Wholesale customers data.csv")

df = load_data()

# ---------------- FEATURE SELECTION ----------------
features = ['Fresh','Milk','Grocery','Frozen','Detergents_Paper','Delicassen']
X = df[features]

# ---------------- SCALING ----------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------- K SELECTION ----------------
st.sidebar.header("Clustering Controls")
k = st.sidebar.slider("Select number of clusters (K)", 2, 8, 4)

# ---------------- MODEL ----------------
kmeans = KMeans(n_clusters=k, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# ---------------- CLUSTER PROFILE ----------------
st.subheader("📊 Cluster Profiles (Average Spend)")
profile = df.groupby("Cluster")[features].mean()
st.dataframe(profile.round(0))

# ---------------- VISUALIZATION ----------------
st.subheader("📈 Cluster Visualization")

x_axis = st.selectbox("X-axis", features, index=2)
y_axis = st.selectbox("Y-axis", features, index=4)

fig, ax = plt.subplots()
scatter = ax.scatter(df[x_axis], df[y_axis],
                     c=df['Cluster'], cmap='viridis', alpha=0.6)

centers = scaler.inverse_transform(kmeans.cluster_centers_)
ax.scatter(centers[:, features.index(x_axis)],
           centers[:, features.index(y_axis)],
           c='red', s=200, marker='X', label='Centroids')

ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
ax.legend()
st.pyplot(fig)

# ---------------- BUSINESS INSIGHTS ----------------
st.subheader("💡 Business Interpretation")

cluster_notes = {
    0: "Fresh-focused Horeca buyers → prioritize perishables & fast replenishment",
    1: "Retail bulk buyers → volume discounts & long-term contracts",
    2: "Balanced buyers → bundle cross-category offers",
    3: "Premium / niche buyers → exclusive products & higher margins"
}

for c in sorted(df['Cluster'].unique()):
    st.markdown(f"**Cluster {c}:** {cluster_notes.get(c, 'Distinct buying behavior')}")

# ---------------- STABILITY CHECK ----------------
st.subheader("🔁 Stability Check")

kmeans_alt = KMeans(n_clusters=k, random_state=99)
df['Alt_Cluster'] = kmeans_alt.fit_predict(X_scaled)

change_rate = (df['Cluster'] != df['Alt_Cluster']).mean()
st.metric("Cluster Change Rate", f"{change_rate*100:.2f}%")

st.caption("Low change rate → stable clustering")
