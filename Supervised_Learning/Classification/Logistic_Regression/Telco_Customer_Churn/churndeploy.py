import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

st.set_page_config(
    page_title="Customer Churn Prediction",
    layout="centered"
)

st.title("📉 Telco Customer Churn Prediction using logestic regression")
st.write("Predict whether a customer is likely to **churn** or **stay**.")

# #Title#
# st.markdown(""" 
# <div class = "card">
#     <h1 class = "title"> <i>Logestic Regression <i> </h1>
#     <p> Predict <b>churn </b> based on <b>features </b> using Logestic Regression. </p>

# </div>

# """,unsafe_allow_html=True)


#Load Data#
@st.cache_data()
def load_data():
    data = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    return data

df= load_data()

#Dataset Preview#
# st.markdown('<div class="card" style="text-align:center">  </div>', unsafe_allow_html=True)
st.subheader("Dataset Preview")
st.dataframe(df.head())
st.markdown('</div>', unsafe_allow_html=True)


# Drop customerID
df.drop("customerID", axis=1, inplace=True)

# Convert TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

# Encode target
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})


features = [
    'tenure',
    'MonthlyCharges',
    'TotalCharges',
    'Contract',
    'PaymentMethod',
    'InternetService'
]

X = df[features]
y = df['Churn']

X = pd.get_dummies(X, drop_first=True)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


st.subheader("📊 Model Performance")

y_pred = model.predict(X_test)

st.write("**Accuracy:**", accuracy_score(y_test, y_pred))
st.write("**Confusion Matrix:**")
st.write(confusion_matrix(y_test, y_pred))

st.text("Classification Report:")
st.text(classification_report(y_test, y_pred))


st.subheader("🧾 Predict Customer Churn")

tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.slider("Monthly Charges", 20.0, 120.0, 70.0)
total_charges = st.slider("Total Charges", 0.0, 9000.0, 1000.0)

contract = st.selectbox("Contract Type", df["Contract"].unique())
payment = st.selectbox("Payment Method", df["PaymentMethod"].unique())
internet = st.selectbox("Internet Service", df["InternetService"].unique())


input_data = pd.DataFrame({
    "tenure": [tenure],
    "MonthlyCharges": [monthly_charges],
    "TotalCharges": [total_charges],
    "Contract": [contract],
    "PaymentMethod": [payment],
    "InternetService": [internet]
})

input_data = pd.get_dummies(input_data)

# Align columns with training data
input_data = input_data.reindex(columns=X.columns, fill_value=0)

# Scale input
input_scaled = scaler.transform(input_data)

# Prediction
prediction = model.predict(input_scaled)[0]
probability = model.predict_proba(input_scaled)[0][1]


if prediction == 1:
    st.error(f"⚠️ Customer is likely to CHURN (Probability: {probability:.2f})")
else:
    st.success(f"✅ Customer is likely to STAY (Probability: {1 - probability:.2f})")


st.subheader("📊 Feature Importance")

importance = pd.Series(
    model.coef_[0],
    index=X.columns
).sort_values()

fig, ax = plt.subplots(figsize=(6,5))
importance.tail(10).plot(kind="barh", ax=ax)
ax.set_title("Top Features Influencing Churn")

st.pyplot(fig)
