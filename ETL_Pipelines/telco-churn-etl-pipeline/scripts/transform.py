# ===========================
# transform.py
# ===========================

import os
import pandas as pd


def transform_data(raw_path):
    # Project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged_dir = os.path.join(base_dir, "data", "staged")
    os.makedirs(staged_dir, exist_ok=True)

    df = pd.read_csv(raw_path)

    # -----------------------
    # Cleaning Tasks
    # -----------------------

    # Convert TotalCharges to numeric
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Fill missing numeric values with median
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill ALL categorical missing values with "Unknown"
    categorical_cols = df.select_dtypes(include="object").columns
    df[categorical_cols] = df[categorical_cols].fillna("Unknown")

    # -----------------------
    # Feature Engineering
    # -----------------------

    # 1. tenure_group
    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[-1, 12, 36, 60, float("inf")],
        labels=["New", "Regular", "Loyal", "Champion"]
    )

    # 2. monthly_charge_segment
    df["monthly_charge_segment"] = pd.cut(
        df["MonthlyCharges"],
        bins=[-1, 30, 70, float("inf")],
        labels=["Low", "Medium", "High"]
    )

    # 3. has_internet_service
    df["has_internet_service"] = df["InternetService"].apply(
        lambda x: 1 if x in ["DSL", "Fiber optic"] else 0
    )

    # 4. is_multi_line_user
    df["is_multi_line_user"] = df["MultipleLines"].apply(
        lambda x: 1 if x == "Yes" else 0
    )

    # 5. contract_type_code
    df["contract_type_code"] = (
        df["Contract"]
        .map({"Month-to-month": 0, "One year": 1, "Two year": 2})
        .fillna(-1)
    )

    # -----------------------
    # Drop unnecessary fields
    # -----------------------
    df.drop(["customerID", "gender"], axis=1, inplace=True)

    # -----------------------
    # Deduplication (IMPORTANT)
    # -----------------------
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"🧹 Deduplicated rows: {before - after}")

    # -----------------------
    # Save output
    # -----------------------
    staged_path = os.path.join(staged_dir, "churn_transformed.csv")
    df.to_csv(staged_path, index=False)

    print(f"✅ Data transformed and saved at: {staged_path}")
    return staged_path


if __name__ == "__main__":
    from extract import extract_data
    raw_path = extract_data()
    transform_data(raw_path)
