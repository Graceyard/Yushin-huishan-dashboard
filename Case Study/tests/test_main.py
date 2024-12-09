import sys
import os
import pytest
import pandas as pd

# Add the src directory to the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import load_data function from your main script
from groupcasestudy_yushin_huishan import load_data

# Test function to check if duplicates are removed in the processed data
def test_no_duplicates():
    """Test if duplicate rows are removed after processing the data."""
    
    # Load the processed datasets
    processed_df_customers, processed_df_order_items, processed_df_orders, processed_df_payments, processed_df_products = load_data()

    # Check if any of the loaded dataframes have duplicates
    assert processed_df_customers.duplicated().sum() == 0, "Duplicate rows found in df_customers"
    assert processed_df_order_items.duplicated().sum() == 0, "Duplicate rows found in df_order_items"
    assert processed_df_orders.duplicated().sum() == 0, "Duplicate rows found in df_orders"
    assert processed_df_payments.duplicated().sum() == 0, "Duplicate rows found in df_payments"
    assert processed_df_products.duplicated().sum() == 0, "Duplicate rows found in df_products"
    
    print("Test passed: No duplicates in processed datasets.")

# Run the test
if __name__ == "__main__":
    pytest.main()