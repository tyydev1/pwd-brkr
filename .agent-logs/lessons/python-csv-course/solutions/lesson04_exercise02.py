"""
Lesson 04 - Exercise 2: Column Addition with Pandas
Solution demonstrating adding calculated columns to a DataFrame
"""

import pandas as pd

def add_calculated_columns(df):
    """
    Add calculated columns to product DataFrame.

    Args:
        df: DataFrame with product, quantity, unit_price columns

    Returns:
        DataFrame with added columns: total_price, tax, final_price
    """
    # Add total_price column
    df['total_price'] = df['quantity'] * df['unit_price']

    # Add tax column (8% of total_price)
    df['tax'] = df['total_price'] * 0.08

    # Add final_price column (total_price + tax)
    df['final_price'] = df['total_price'] + df['tax']

    # Round to 2 decimal places for currency
    df['total_price'] = df['total_price'].round(2)
    df['tax'] = df['tax'].round(2)
    df['final_price'] = df['final_price'].round(2)

    return df


def create_sample_data():
    """Create sample product data"""
    data = {
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam'],
        'quantity': [2, 5, 3, 1, 4],
        'unit_price': [999.99, 29.99, 79.99, 299.99, 89.99]
    }
    return pd.DataFrame(data)


# Main execution
if __name__ == "__main__":
    print("Creating sample product data...\n")

    # Create sample data
    df = create_sample_data()

    print("Original Data:")
    print(df)
    print()

    # Add calculated columns
    df_enhanced = add_calculated_columns(df)

    print("Data with Calculated Columns:")
    print(df_enhanced)
    print()

    # Save to CSV
    output_file = 'products_with_calculations.csv'
    df_enhanced.to_csv(output_file, index=False)

    print(f"Enhanced data saved to: {output_file}")

    # Display summary statistics
    print("\nSummary Statistics:")
    print(f"Total Revenue (before tax): ${df_enhanced['total_price'].sum():,.2f}")
    print(f"Total Tax: ${df_enhanced['tax'].sum():,.2f}")
    print(f"Total Revenue (with tax): ${df_enhanced['final_price'].sum():,.2f}")
    print(f"Average Order Value: ${df_enhanced['final_price'].mean():,.2f}")
