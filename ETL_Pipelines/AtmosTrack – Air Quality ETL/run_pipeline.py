# run_pipeline.py
from extract import extract
from transform import transform
from load import load
from etl_analysis import analyze

if __name__ == "__main__":
    extract()
    transform()
    load()
    analyze()
    print("🚀 Air Quality ETL Pipeline Completed Successfully")
