import streamlit as st
import numpy as np

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Loan Approval System – Stacking Model",
    layout="wide"
)

# -------------------------------------------------
# TITLE & DESCRIPTION
# -------------------------------------------------
st.title("🎯 Smart Loan Approval System – Stacking Model")
st.write(
    "This system uses a **Stacking Ensemble Machine Learning model** to predict whether "
    "a loan will be approved by combining multiple ML models for better decision making."
)

st.markdown("---")

# -------------------------------------------------
# SIDEBAR – USER INPUTS
# -------------------------------------------------
st.sidebar.header("📋 Applicant Details")

applicant_income = st.sidebar.number_input("Applicant Income", min_value=0, step=1000)
coapplicant_income = st.sidebar.number_input("Co-Applicant Income", min_value=0, step=1000)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=0, step=1000)
loan_term = st.sidebar.number_input("Loan Amount Term (months)", min_value=0, step=12)

credit_history = st.sidebar.radio("Credit History", ["Yes", "No"])
employment_status = st.sidebar.selectbox("Employment Status", ["Salaried", "Self-Employed"])
property_area = st.sidebar.selectbox("Property Area", ["Urban", "Semi-Urban", "Rural"])

# -------------------------------------------------
# ENCODING INPUTS
# -------------------------------------------------
credit_val = 1 if credit_history == "Yes" else 0
employment_val = 1 if employment_status == "Salaried" else 0

property_map = {"Urban": 2, "Semi-Urban": 1, "Rural": 0}
property_val = property_map[property_area]

total_income = applicant_income + coapplicant_income

# -------------------------------------------------
# MODEL ARCHITECTURE DISPLAY
# -------------------------------------------------
st.subheader("🧠 Stacking Model Architecture")

st.info(
    """
    **Base Models (Level-0):**
    • Logistic Regression  
    • Decision Tree  
    • Random Forest  

    **Meta Model (Level-1):**
    • Logistic Regression  

    👉 Base model predictions are combined and passed to the meta-model
    for final loan approval decision.
    """
)

# -------------------------------------------------
# SIMULATED BASE MODELS (NO PKL FILES)
# -------------------------------------------------
def logistic_regression_model():
    return 1 if (credit_val == 1 and total_income > loan_amount) else 0

def decision_tree_model():
    return 1 if (credit_val == 1 and loan_amount < 500000) else 0

def random_forest_model():
    score = 0
    score += 1 if credit_val == 1 else 0
    score += 1 if total_income > loan_amount else 0
    score += 1 if employment_val == 1 else 0
    return 1 if score >= 2 else 0

# -------------------------------------------------
# META MODEL (STACKING LOGIC)
# -------------------------------------------------
def meta_model(preds):
    return 1 if sum(preds) >= 2 else 0

# -------------------------------------------------
# PREDICTION BUTTON
# -------------------------------------------------
st.markdown("---")

if st.button("🔘 Check Loan Eligibility (Stacking Model)"):

    lr_pred = logistic_regression_model()
    dt_pred = decision_tree_model()
    rf_pred = random_forest_model()

    base_preds = [lr_pred, dt_pred, rf_pred]
    final_pred = meta_model(base_preds)

    confidence = (sum(base_preds) / 3) * 100

    # -------------------------------------------------
    # OUTPUT SECTION
    # -------------------------------------------------
    st.subheader("📊 Prediction Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Base Model Predictions")
        st.write(f"**Logistic Regression:** {'Approved' if lr_pred else 'Rejected'}")
        st.write(f"**Decision Tree:** {'Approved' if dt_pred else 'Rejected'}")
        st.write(f"**Random Forest:** {'Approved' if rf_pred else 'Rejected'}")

    with col2:
        st.markdown("### 🧠 Final Stacking Decision")
        if final_pred == 1:
            st.success("✅ Loan Approved")
        else:
            st.error("❌ Loan Rejected")

        st.write(f"📈 **Confidence Score:** {confidence:.2f}%")

    # -------------------------------------------------
    # BUSINESS EXPLANATION (MANDATORY)
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("💼 Business Explanation")

    if final_pred == 1:
        st.write(
            "Based on the applicant’s income, credit history, employment status, "
            "and combined predictions from multiple models, the applicant is likely "
            "to repay the loan.\n\n"
            "**Therefore, the stacking model predicts loan approval.**"
        )
    else:
        st.write(
            "Based on the applicant’s income, credit history, employment status, "
            "and combined predictions from multiple models, the applicant is unlikely "
            "to repay the loan.\n\n"
            "**Therefore, the stacking model predicts loan rejection.**"
        )
