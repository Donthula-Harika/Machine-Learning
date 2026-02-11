# app.py
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# -----------------------------
# App Header
# -----------------------------
st.set_page_config(page_title="Customer Risk Prediction System (KNN)")

st.title("Customer Risk Prediction System (KNN)")
st.write("This system predicts customer risk by comparing them with similar customers.")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("loan_data.csv")   # change name if needed

# -----------------------------
# Feature Selection
# -----------------------------
X = df[
    ['person_age',
     'person_income',
     'loan_amnt',
     'cb_person_cred_hist_length']
]

y = df['loan_status']   # 1 = High Risk, 0 = Low Risk

# -----------------------------
# Train-Test Split
# -----------------------------
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Scaling
# -----------------------------
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Customer Input")

age = st.sidebar.slider("Age", 18, 100, 30)
income = st.sidebar.number_input("Annual Income", min_value=0, step=50000)
loan_amt = st.sidebar.number_input("Loan Amount", min_value=0, step=10000)
credit_history = st.sidebar.selectbox("Credit History", ["Yes", "No"])
k = st.sidebar.slider("K Value", 1, 15, 5)

credit_hist_len = 5 if credit_history == "Yes" else 0

# -----------------------------
# Prediction Button
# -----------------------------
if st.button("Predict Customer Risk"):

    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(x_train, y_train)

    new_customer = np.array([[
        age,
        income,
        loan_amt,
        credit_hist_len
    ]])

    new_customer_scaled = scaler.transform(new_customer)

    prediction = knn.predict(new_customer_scaled)[0]

    # -----------------------------
    # Prediction Output
    # -----------------------------
    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("🔴 High Risk Customer")
    else:
        st.success("🟢 Low Risk Customer")

    # -----------------------------
    # Nearest Neighbors Explanation
    # -----------------------------
    distances, indices = knn.kneighbors(new_customer_scaled)
    neighbor_labels = y_train.iloc[indices[0]]

    st.subheader("Nearest Neighbors Explanation")
    st.write(f"Number of neighbors considered: **{k}**")

    majority = "High Risk" if neighbor_labels.mean() > 0.5 else "Low Risk"
    st.write(f"Majority class among neighbors: **{majority}**")

    st.write("Nearest similar customers:")
    st.dataframe(
        df.iloc[indices[0]][
            ['person_age', 'person_income', 'loan_amnt', 'loan_status']
        ]
    )

    # -----------------------------
    # Business Insight
    # -----------------------------
    st.info(
        "This decision is based on similarity with nearby customers in feature space."
    )
