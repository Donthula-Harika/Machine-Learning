# validate.py
# Purpose: Validate Supabase churn data against transformed dataset

import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv


# ---------------------------
# Supabase client
# ---------------------------
def get_supabase_client():
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("❌ Missing Supabase credentials")

    return create_client(url, key)


# ---------------------------
# Fetch full Supabase table
# ---------------------------
def fetch_supabase_table(table_name="telco_customer_data"):
    supabase = get_supabase_client()

    rows = []
    offset = 0
    page_size = 1000

    while True:
        resp = (
            supabase
            .table(table_name)
            .select("*")
            .range(offset, offset + page_size - 1)
            .execute()
        )

        data = resp.data or []
        if not data:
            break

        rows.extend(data)
        if len(data) < page_size:
            break

        offset += page_size

    return pd.DataFrame(rows)


# ---------------------------
# Validation Runner
# ---------------------------
if __name__ == "__main__":

    staged_path = os.path.join("..", "data", "staged", "churn_transformed.csv")
    if not os.path.exists(staged_path):
        raise FileNotFoundError("❌ Transformed CSV not found")

    df_original = pd.read_csv(staged_path)
    df_loaded = fetch_supabase_table()

    print("\n🔎 VALIDATION SUMMARY")
    print("---------------------")

    # 1️⃣ No missing values
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    missing_numeric = df_loaded[numeric_cols].isna().sum().sum()
    print(
        "✅ No missing values in tenure, MonthlyCharges, TotalCharges"
        if missing_numeric == 0
        else f"❌ Missing numeric values found: {missing_numeric}"
    )

    # 2️⃣ Unique count of rows
    orig_unique = len(df_original.drop_duplicates())
    loaded_unique = len(df_loaded.drop_duplicates())
    print(
        f"✅ Unique row count matches: {orig_unique}"
        if orig_unique == loaded_unique
        else f"❌ Unique row count mismatch: original={orig_unique}, Supabase={loaded_unique}"
    )

    # 3️⃣ Row count match
    print(
        f"✅ Row count matches: {len(df_original)}"
        if len(df_original) == len(df_loaded)
        else f"❌ Row count mismatch: original={len(df_original)}, Supabase={len(df_loaded)}"
    )

    # 4️⃣ Segment checks
    tenure_ok = set(df_loaded["tenure_group"]) == {"New", "Regular", "Loyal", "Champion"}
    charge_ok = set(df_loaded["monthly_charge_segment"]) == {"Low", "Medium", "High"}

    if tenure_ok and charge_ok:
        print("✅ All tenure_group and monthly_charge_segment values exist")
    else:
        print("❌ Missing segments detected")

    # 5️⃣ Contract code validation
    valid_codes = {0, 1, 2}
    actual_codes = set(df_loaded["contract_type_code"].dropna())

    print(
        "✅ Contract codes valid: {0,1,2}"
        if actual_codes.issubset(valid_codes)
        else f"❌ Invalid contract codes found: {actual_codes - valid_codes}"
    )

    print("\n🎯 Validation complete.")
