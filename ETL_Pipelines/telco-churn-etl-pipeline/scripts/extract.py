import os
import seaborn as sns
import pandas as pd
 
def extract_data():
    #project root directory is based on the location of this script
    #this allows the script to be run from anywhere in the project  
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #Purpose: Gets the project root directory
    print(f"Base directory: {base_dir}")

    data_dir = os.path.join(base_dir, "data", "raw")    #Purpose: Builds this folder path:project_root/data/raw
    os.makedirs(data_dir, exist_ok=True) #Purpose: Creates the folder if it doesn’t exist
    print(f"Data directory: {data_dir}")

    df = pd.read_csv("D:\TekWorks\MACHINE LEARNING\Transform\WA_Fn-UseC_-Telco-Customer-Churn.csv") #Purpose: Reads the CSV file into a DataFrame
    raw_path = os.path.join(data_dir, "Telco-Customer-Churn.csv")  #Purpose: Builds this file path: project_root/data/raw/titanic_raw.csv
    print("raw path:", raw_path)

    df.to_csv(raw_path, index=False) #Purpose: Saves the DataFrame as a CSV file at the constructed path
 
    print(f"✅ Data extracted and saved at: {raw_path}")
    return raw_path
 
if __name__ == "__main__":
    extract_data()
 