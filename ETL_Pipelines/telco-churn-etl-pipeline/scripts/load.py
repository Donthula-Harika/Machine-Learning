
# ===========================
# load.py
# ===========================
# Purpose: Load transformed churn data into Supabase

import os
import time
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
        raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_KEY")

    return create_client(url, key)


# ---------------------------
# Load data to Supabase
# ---------------------------
def load_to_supabase(
    staged_csv_path,
    table_name="telco_customer_data",
    batch_size=200
):
    supabase = get_supabase_client()

    # Load transformed data
    df = pd.read_csv(staged_csv_path)

    # Convert NaN → None
    df = df.where(pd.notnull(df), None)

    total_rows = len(df)
    print(f"📊 Loading {total_rows} rows into Supabase table '{table_name}'")

    # Insert in batches
    for start in range(0, total_rows, batch_size):
        end = start + batch_size
        batch_df = df.iloc[start:end]
        records = batch_df.to_dict(orient="records")

        # Retry logic (max 3 attempts)
        for attempt in range(3):
            try:
                supabase.table(table_name).insert(records).execute()
                print(f"✅ Inserted rows {start + 1}–{min(end, total_rows)}")
                break
            except Exception as e:
                if attempt == 2:
                    print(
                        f"❌ Failed batch {start // batch_size + 1}: {e}"
                    )
                time.sleep(2 ** attempt)

    print("🎯 Data load completed successfully")


# ---------------------------
# Run as script
# ---------------------------
if __name__ == "__main__":
    staged_path = os.path.join("..", "data", "staged", "churn_transformed.csv")

    if not os.path.exists(staged_path):
        raise FileNotFoundError(
            "❌ Transformed CSV not found. Run transform.py first."
        )

    load_to_supabase(staged_path)
