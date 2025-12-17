# load.py
import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
from math import isnan
from time import sleep

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

TABLE = "air_quality_data2"
BATCH_SIZE = 200

def load():
    df = pd.read_csv("data/staged/air_quality_transformed.csv")
    df = df.where(pd.notnull(df), None)

    total = 0
    for i in range(0, len(df), BATCH_SIZE):
        batch = df.iloc[i:i+BATCH_SIZE].to_dict("records")

        for _ in range(2):
            try:
                supabase.table(TABLE).insert(batch).execute()
                total += len(batch)
                break
            except Exception:
                sleep(2)

    print(f"✅ Inserted {total} rows")

if __name__ == "__main__":
    load()
