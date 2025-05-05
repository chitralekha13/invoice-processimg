import pandas as pd
import numpy as np

def preprocess_training_data(csv_path):
    # Load the dataset
    df = pd.read_csv(csv_path)

    # Handle missing values
    df.fillna("", inplace=True)

    # Feature engineering: Convert dates into datetime objects
    date_cols = ["Invoice Date", "Baseline Date", "Due Date"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Drop rows with invalid dates
    df.dropna(subset=date_cols, inplace=True)

    # Create numeric fields for training (e.g., days until due date)
    df["Days Until Due"] = (df["Due Date"] - df["Invoice Date"]).dt.days

    # Convert categorical features into numeric
    df["Customer ID"] = df["Customer ID"].astype("category").cat.codes

    # Return the processed dataframe
    return df

# Example usage
if __name__ == "__main__":
    training_data_path = "./data/training/customer_invoices.csv"
    processed_data = preprocess_training_data(training_data_path)
    processed_data.to_csv("./data/training/processed_customer_invoices.csv", index=False)
    print("Training data preprocessed and saved.")
