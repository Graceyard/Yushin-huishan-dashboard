import pandas as pd
import os

def load_and_process_data(filepath, output_path):
    """
    Loads the dataset, removes duplicate rows, and saves the processed dataset.

    Args:
        filepath (str): Path to the input dataset.
        output_path (str): Path to save the processed dataset.

    Returns:
        pd.DataFrame: Processed DataFrame with no duplicates.
    """
    # Load the dataset
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")

    df = pd.read_csv(filepath)
    print(f"Original dataset shape ({filepath}): {df.shape}")

    # Remove duplicate rows
    df = df.drop_duplicates()
    print(f"Dataset shape after removing duplicates: {df.shape}")

    # Save the processed dataset
    output_path = os.path.abspath(output_path)
    try:
        print(f"Attempting to save to: {output_path}")
        df.to_csv(output_path, index=False)
        print(f"Processed dataset for {filepath} saved successfully!")
    except Exception as e:
        print(f"Failed to save file. Error: {e}")

    return df

def process_all_files():
    # List of input files and corresponding output files
    files = [
        ('Ecommerce Order Dataset/df_Customers.csv', 'Ecommerce Order Dataset/processed_df_Customers.csv'),
        ('Ecommerce Order Dataset/df_Orderitems.csv', 'Ecommerce Order Dataset/processed_df_Orderitems.csv'),
        ('Ecommerce Order Dataset/df_Orders.csv', 'Ecommerce Order Dataset/processed_df_Orders.csv'),
        ('Ecommerce Order Dataset/df_Payments.csv', 'Ecommerce Order Dataset/processed_df_Payments.csv'),
        ('Ecommerce Order Dataset/df_Products.csv', 'Ecommerce Order Dataset/processed_df_Products.csv')
    ]

    # Loop through each file and process it
    for input_file, output_file in files:
        load_and_process_data(input_file, output_file)

if __name__ == "__main__":
    process_all_files()