# etl_analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def analyze():
    resp = supabase.table("air_quality_data").select("*").range(0, 100000).execute()
    df = pd.DataFrame(resp.data)

    os.makedirs("data/processed", exist_ok=True)

    summary = {
        "highest_avg_pm25": df.groupby("city")["pm2_5"].mean().idxmax(),
        "highest_severity_city": df.groupby("city")["severity_score"].mean().idxmax(),
    }

    risk_dist = df.groupby(["city","risk_flag"]).size().reset_index(name="count")
    trends = df[["city","time","pm2_5","pm10","ozone"]]

    pd.DataFrame([summary]).to_csv("data/processed/summary_metrics.csv", index=False)
    risk_dist.to_csv("data/processed/city_risk_distribution.csv", index=False)
    trends.to_csv("data/processed/pollution_trends.csv", index=False)

    df["pm2_5"].hist()
    plt.savefig("data/processed/pm25_hist.png")
    plt.clf()

    risk_dist.pivot(index="city", columns="risk_flag", values="count").plot(kind="bar")
    plt.savefig("data/processed/risk_bar.png")
    plt.clf()

    df.groupby("time")["pm2_5"].mean().plot()
    plt.savefig("data/processed/pm25_trend.png")
    plt.clf()

    plt.scatter(df["pm2_5"], df["severity_score"])
    plt.savefig("data/processed/severity_scatter.png")

if __name__ == "__main__":
    analyze()
