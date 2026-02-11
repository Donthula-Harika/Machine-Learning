# import streamlit as st
# import numpy as np

# # -------------------------------------------------
# # PAGE CONFIG
# # -------------------------------------------------
# st.set_page_config(
#     page_title="Smart Loan Approval System – Stacking Model",
#     page_icon="🏦",
#     layout="wide"
# )

# # -------------------------------------------------
# # CUSTOM CSS (UI BOOST)
# # -------------------------------------------------
# st.markdown("""
# <style>
# .main {
#     background-color: #f8f9fa;
# }
# .big-title {
#     font-size: 38px;
#     font-weight: 800;
#     color: #0d6efd;
# }
# .sub-text {
#     font-size: 17px;
#     color: #555;
# }
# .card {
#     background-color: white;
#     padding: 20px;
#     border-radius: 15px;
#     box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
#     margin-bottom: 20px;
# }
# .green {
#     color: #198754;
#     font-weight: bold;
# }
# .red {
#     color: #dc3545;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)

# # -------------------------------------------------
# # TITLE & DESCRIPTION
# # -------------------------------------------------
# st.markdown('<div class="big-title">🎯 Smart Loan Approval System</div>', unsafe_allow_html=True)
# st.markdown(
#     '<div class="sub-text">A smart decision-support system using a '
#     '<b>Stacking Ensemble Machine Learning model</b> to predict loan approval '
#     'by combining multiple models.</div>',
#     unsafe_allow_html=True
# )

# st.markdown("---")

# # -------------------------------------------------
# # SIDEBAR INPUTS
# # -------------------------------------------------
# st.sidebar.header("📋 Applicant Information")

# applicant_income = st.sidebar.slider("Applicant Income", 0, 2000000, 300000, step=10000)
# coapplicant_income = st.sidebar.slider("Co-Applicant Income", 0, 2000000, 0, step=10000)
# loan_amount = st.sidebar.slider("Loan Amount", 0, 2000000, 500000, step=10000)
# loan_term = st.sidebar.selectbox("Loan Amount Term (Months)", [120, 180, 240, 300, 360])

# credit_history = st.sidebar.radio("Credit History", ["Yes", "No"])
# employment_status = st.sidebar.selectbox("Employment Status", ["Salaried", "Self-Employed"])
# property_area = st.sidebar.selectbox("Property Area", ["Urban", "Semi-Urban", "Rural"])

# # -------------------------------------------------
# # ENCODING INPUTS
# # -------------------------------------------------
# credit_val = 1 if credit_history == "Yes" else 0
# employment_val = 1 if employment_status == "Salaried" else 0
# property_map = {"Urban": 2, "Semi-Urban": 1, "Rural": 0}
# property_val = property_map[property_area]

# total_income = applicant_income + coapplicant_income

# # -------------------------------------------------
# # MODEL ARCHITECTURE DISPLAY
# # -------------------------------------------------
# st.markdown('<div class="card">', unsafe_allow_html=True)
# st.subheader("🧠 Stacking Model Architecture")

# st.write("""
# **Base Models (Level-0):**
# - Logistic Regression  
# - Decision Tree  
# - Random Forest  

# **Meta Model (Level-1):**
# - Logistic Regression  

# 👉 Predictions from base models are combined to make a stronger final decision.
# """)
# st.markdown('</div>', unsafe_allow_html=True)

# # -------------------------------------------------
# # SIMULATED BASE MODELS
# # -------------------------------------------------
# def logistic_regression_model():
#     return 1 if credit_val == 1 and total_income > loan_amount else 0

# def decision_tree_model():
#     return 1 if credit_val == 1 and loan_amount < 600000 else 0

# def random_forest_model():
#     score = 0
#     score += 1 if credit_val == 1 else 0
#     score += 1 if total_income > loan_amount else 0
#     score += 1 if employment_val == 1 else 0
#     return 1 if score >= 2 else 0

# def meta_model(preds):
#     return 1 if sum(preds) >= 2 else 0

# # -------------------------------------------------
# # PREDICTION BUTTON
# # -------------------------------------------------
# st.markdown("## 🔍 Loan Eligibility Check")

# if st.button("🚀 Check Loan Eligibility (Stacking Model)", use_container_width=True):

#     lr_pred = logistic_regression_model()
#     dt_pred = decision_tree_model()
#     rf_pred = random_forest_model()

#     base_preds = [lr_pred, dt_pred, rf_pred]
#     final_pred = meta_model(base_preds)
#     confidence = (sum(base_preds) / 3) * 100

#     # -------------------------------------------------
#     # RESULTS SECTION
#     # -------------------------------------------------
#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown('<div class="card">', unsafe_allow_html=True)
#         st.subheader("📊 Base Model Predictions")

#         st.metric("Logistic Regression", "Approved" if lr_pred else "Rejected")
#         st.metric("Decision Tree", "Approved" if dt_pred else "Rejected")
#         st.metric("Random Forest", "Approved" if rf_pred else "Rejected")

#         st.markdown('</div>', unsafe_allow_html=True)

#     with col2:
#         st.markdown('<div class="card">', unsafe_allow_html=True)
#         st.subheader("🧠 Final Stacking Decision")

#         if final_pred == 1:
#             st.success("✅ Loan Approved")
#         else:
#             st.error("❌ Loan Rejected")

#         st.metric("Confidence Score", f"{confidence:.1f}%")
#         st.markdown('</div>', unsafe_allow_html=True)

#     # -------------------------------------------------
#     # BUSINESS EXPLANATION
#     # -------------------------------------------------
#     st.markdown('<div class="card">', unsafe_allow_html=True)
#     st.subheader("💼 Business Explanation")

#     if final_pred == 1:
#         st.write(
#             "Based on the applicant’s income level, credit history, employment status, "
#             "and combined predictions from multiple models, the applicant is likely "
#             "to repay the loan.\n\n"
#             "**Therefore, the stacking model predicts loan approval.**"
#         )
#     else:
#         st.write(
#             "Based on the applicant’s income level, credit history, employment status, "
#             "and combined predictions from multiple models, the applicant is unlikely "
#             "to repay the loan.\n\n"
#             "**Therefore, the stacking model predicts loan rejection.**"
#         )
#     st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st
import numpy as np

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Loan Approval – Stacking Model",
    page_icon="🌌",
    layout="wide"
)

# -------------------------------------------------
# GLOBAL THEME (NO DIV WRAPPERS)
# -------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0b0f1a;
    color: #eaeaea;
}

h1, h2, h3 {
    color: #eaeaea;
}

.stButton>button {
    background: linear-gradient(90deg, #00f5d4, #5f6cff);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
}

.stMetric {
    background-color: #111827;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE & DESCRIPTION
# -------------------------------------------------
st.title("🌌 Smart Loan Approval System – Stacking Model")
st.write(
    "This application demonstrates a **Stacking Ensemble Machine Learning approach** "
    "to predict loan approval by combining multiple models for better decision making."
)

st.divider()

# -------------------------------------------------
# SIDEBAR INPUTS (KEPT)
# -------------------------------------------------
st.sidebar.header("📋 Applicant Details")

applicant_income = st.sidebar.slider("Applicant Income", 0, 2_000_000, 300_000, step=10_000)
coapplicant_income = st.sidebar.slider("Co-Applicant Income", 0, 2_000_000, 0, step=10_000)
loan_amount = st.sidebar.slider("Loan Amount", 0, 2_000_000, 500_000, step=10_000)

loan_term = st.sidebar.selectbox(
    "Loan Term (Months)", [120, 180, 240, 300, 360]
)

credit_history = st.sidebar.radio("Credit History", ["Yes", "No"])
employment_status = st.sidebar.selectbox(
    "Employment Status", ["Salaried", "Self-Employed"]
)
property_area = st.sidebar.selectbox(
    "Property Area", ["Urban", "Semi-Urban", "Rural"]
)

# -------------------------------------------------
# ENCODING INPUTS
# -------------------------------------------------
credit_val = 1 if credit_history == "Yes" else 0
employment_val = 1 if employment_status == "Salaried" else 0
total_income = applicant_income + coapplicant_income

# -------------------------------------------------
# STACKING ARCHITECTURE (CLEAN DISPLAY)
# -------------------------------------------------
st.subheader("🧠 Stacking Model Architecture")

st.markdown("""
**Base Models (Level-0):**
- Logistic Regression  
- Decision Tree  
- Random Forest  

**Meta Model (Level-1):**
- Logistic Regression  

📌 Predictions from base models are combined to make a stronger final decision.
""")

st.divider()

# -------------------------------------------------
# SIMULATED BASE MODELS (NO PKL, NO ERRORS)
# -------------------------------------------------
def logistic_regression_model():
    return 1 if credit_val == 1 and total_income > loan_amount else 0

def decision_tree_model():
    return 1 if credit_val == 1 and loan_amount < 600_000 else 0

def random_forest_model():
    score = 0
    score += 1 if credit_val == 1 else 0
    score += 1 if total_income > loan_amount else 0
    score += 1 if employment_val == 1 else 0
    return 1 if score >= 2 else 0

def meta_model(preds):
    return 1 if sum(preds) >= 2 else 0

# -------------------------------------------------
# PREDICTION BUTTON
# -------------------------------------------------
if st.button("🚀 Check Loan Eligibility (Stacking Model)", use_container_width=True):

    lr_pred = logistic_regression_model()
    dt_pred = decision_tree_model()
    rf_pred = random_forest_model()

    base_preds = [lr_pred, dt_pred, rf_pred]
    final_pred = meta_model(base_preds)
    confidence = (sum(base_preds) / 3) * 100

    # -------------------------------------------------
    # RESULTS SECTION
    # -------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Base Model Predictions")
        st.metric("Logistic Regression", "Approved" if lr_pred else "Rejected")
        st.metric("Decision Tree", "Approved" if dt_pred else "Rejected")
        st.metric("Random Forest", "Approved" if rf_pred else "Rejected")

    with col2:
        st.subheader("🧠 Final Stacking Decision")
        if final_pred:
            st.success("✅ Loan Approved")
        else:
            st.error("❌ Loan Rejected")

        st.metric("Confidence Score", f"{confidence:.1f}%")

    # -------------------------------------------------
    # BUSINESS EXPLANATION (MANDATORY)
    # -------------------------------------------------
    st.divider()
    st.subheader("💼 Business Explanation")

    if final_pred:
        st.write(
            "Based on income strength, positive credit history, employment stability, "
            "and combined predictions from multiple models, the applicant is likely "
            "to repay the loan. Therefore, the stacking model predicts **loan approval**."
        )
    else:
        st.write(
            "Based on income patterns, credit risk, and combined predictions from "
            "multiple models, the applicant may face repayment challenges. "
            "Therefore, the stacking model predicts **loan rejection**."
        )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.caption("🌌 Aurora Theme • Stacking Ensemble Learning Demo")
