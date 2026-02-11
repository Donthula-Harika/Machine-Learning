import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="NYC Taxi Pickup Clustering",
    layout="wide"
)

st.title("🚕 NYC Taxi Pickup Hotspot Discovery")
st.caption("Density-based clustering using DBSCAN")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("NewYorkCityTaxiTripDuration (1).csv")

df = load_data()

with st.expander("📄 Dataset Preview"):
    st.dataframe(df.head(), use_container_width=True)

# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------
st.sidebar.header("⚙️ Controls")

sample_size = st.sidebar.slider(
    "Sample size (performance control)",
    min_value=3000,
    max_value=20000,
    value=10000,
    step=1000
)

eps = st.sidebar.slider(
    "DBSCAN eps (neighborhood radius)",
    min_value=0.1,
    max_value=1.0,
    value=0.4,
    step=0.05
)

min_samples = st.sidebar.slider(
    "min_samples",
    min_value=3,
    max_value=20,
    value=5
)

run = st.sidebar.button("🚀 Run Clustering")

# --------------------------------------------------
# Data Preparation
# --------------------------------------------------
df_sample = df.sample(n=sample_size, random_state=42)
X = df_sample[["pickup_latitude", "pickup_longitude"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X).astype("float32")

# --------------------------------------------------
# Run DBSCAN
# --------------------------------------------------
if run:
    with st.spinner("Clustering pickup locations..."):
        model = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            algorithm="ball_tree"
        )
        labels = model.fit_predict(X_scaled)

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------
    clusters = len(set(labels)) - (1 if -1 in labels else 0)
    noise = np.sum(labels == -1)
    noise_ratio = noise / len(labels)

    col1, col2, col3 = st.columns(3)
    col1.metric("Clusters", clusters)
    col2.metric("Noise Points", noise)
    col3.metric("Noise Ratio", f"{noise_ratio:.2f}")

    if clusters > 1:
        mask = labels != -1
        score = silhouette_score(X_scaled[mask], labels[mask])
        st.success(f"Silhouette Score: {score:.3f}")
    else:
        st.warning("Silhouette Score: Not Applicable")

    # --------------------------------------------------
    # Visualization
    # --------------------------------------------------
    st.subheader("📍 Pickup Location Clusters")

    fig, ax = plt.subplots(figsize=(9, 6))

    for label in set(labels):
        mask = labels == label
        if label == -1:
            ax.scatter(
                X.iloc[mask, 1],
                X.iloc[mask, 0],
                c="black",
                s=6,
                label="Noise"
            )
        else:
            ax.scatter(
                X.iloc[mask, 1],
                X.iloc[mask, 0],
                s=6,
                label=f"Cluster {label}"
            )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(f"DBSCAN Result (eps={eps}, min_samples={min_samples})")
    ax.legend(markerscale=2)
    st.pyplot(fig)

# --------------------------------------------------
# Insight Section
# --------------------------------------------------
st.markdown("---")
st.subheader("🧠 How to Interpret This")

st.markdown("""
- **Clusters** represent high-density pickup hotspots  
- **Noise points** are rare or isolated pickups  
- **Lower eps** → more clusters, more noise  
- **Higher eps** → fewer, larger clusters  

This model helps identify:
- Taxi demand hotspots  
- Urban mobility patterns  
- Potential ride-sharing zones  
""")
