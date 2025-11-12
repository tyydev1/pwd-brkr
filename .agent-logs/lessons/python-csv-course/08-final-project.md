# Lesson 08: Final Project - CSV Data Processor

## Project Overview

Congratulations on reaching the final lesson! Now you'll apply everything you've learned to build a complete, professional-grade CSV data processing application. This project simulates a real-world scenario: building a sales data processor for an e-commerce company.

The project combines all skills from this course:
- Reading and writing CSV files
- Data validation and cleaning
- Transformation and calculation
- Error handling and logging
- Performance optimization
- Best practices

## Project Scenario

You work for an e-commerce company that receives daily sales data from multiple regional offices. Your task is to build a robust data processor that:

1. Consolidates sales data from multiple CSV files
2. Enriches data with product and customer information
3. Cleans and validates the data
4. Calculates business metrics
5. Generates summary reports
6. Handles errors gracefully and logs all operations

## Project Requirements

### Input Files

Your processor should handle these CSV files:

**1. Sales Files** (sales_region_A.csv, sales_region_B.csv, etc.)
```csv
order_id,product_id,customer_id,quantity,order_date
1001,P001,C101,2,2024-01-15
1002,P002,C102,1,2024-01-15
```

**2. Products File** (products.csv)
```csv
product_id,product_name,category,unit_price,cost
P001,Laptop,Electronics,999.99,600.00
P002,Mouse,Accessories,25.99,10.00
```

**3. Customers File** (customers.csv)
```csv
customer_id,name,email,city,country,join_date
C101,Alice Johnson,alice@email.com,New York,USA,2023-06-15
C102,Bob Smith,bob@email.com,London,UK,2023-08-20
```

### Required Features

#### Feature 1: Data Loading and Validation
- Load all sales files from a directory
- Validate required columns exist
- Handle encoding issues
- Report any malformed files
- Skip completely invalid files but log them

#### Feature 2: Data Consolidation
- Combine multiple sales files into one dataset
- Add source file information to track origin
- Handle duplicate order_ids appropriately
- Preserve data integrity

#### Feature 3: Data Enrichment
- Merge sales with product information
- Merge sales with customer information
- Handle missing references (products/customers not found)
- Flag records with missing data

#### Feature 4: Data Cleaning
- Handle missing values appropriately
- Convert data types correctly (dates, numbers)
- Standardize formats (dates, country names)
- Remove or flag invalid records

#### Feature 5: Calculations
Calculate these metrics:
- **Revenue**: quantity × unit_price
- **Profit**: revenue - (quantity × cost)
- **Profit Margin**: profit / revenue
- **Days Since Customer Joined**: order_date - join_date

#### Feature 6: Summary Reports

Generate three CSV reports:

**A. Detailed Transactions** (sales_detailed.csv)
- All original data plus enrichments and calculations
- One row per order

**B. Product Performance** (product_summary.csv)
- Total revenue per product
- Total quantity sold
- Average order size
- Total profit
- Profit margin

**C. Customer Analysis** (customer_summary.csv)
- Total orders per customer
- Total revenue per customer
- Average order value
- Customer lifetime value
- Most purchased category

#### Feature 7: Error Handling and Logging
- Comprehensive logging to file and console
- Track processing statistics
- Report validation failures
- Handle all exceptions gracefully
- Never crash the program

#### Feature 8: Performance
- Process large files efficiently (chunking if needed)
- Optimize memory usage
- Complete processing in reasonable time

## Project Structure

```
csv_processor/
├── processor.py          # Main processor class
├── validator.py          # Data validation functions
├── utils.py              # Utility functions (encoding detection, etc.)
├── config.py             # Configuration constants
├── main.py               # Entry point
├── data/                 # Input data directory
│   ├── sales/
│   │   ├── sales_region_A.csv
│   │   ├── sales_region_B.csv
│   │   └── sales_region_C.csv
│   ├── products.csv
│   └── customers.csv
├── output/               # Generated reports
│   ├── sales_detailed.csv
│   ├── product_summary.csv
│   └── customer_summary.csv
└── logs/
    └── processor.log     # Processing logs
```

## Implementation Guide

### Step 1: Setup and Configuration

Create `config.py`:
```python
from pathlib import Path

# Directory paths
DATA_DIR = Path('data')
SALES_DIR = DATA_DIR / 'sales'
OUTPUT_DIR = Path('output')
LOG_DIR = Path('logs')

# File paths
PRODUCTS_FILE = DATA_DIR / 'products.csv'
CUSTOMERS_FILE = DATA_DIR / 'customers.csv'

# Required columns
SALES_REQUIRED_COLS = ['order_id', 'product_id', 'customer_id', 'quantity', 'order_date']
PRODUCTS_REQUIRED_COLS = ['product_id', 'product_name', 'category', 'unit_price', 'cost']
CUSTOMERS_REQUIRED_COLS = ['customer_id', 'name', 'email', 'city', 'country', 'join_date']

# Processing options
CHUNK_SIZE = 10000  # For large file processing
ENCODINGS_TO_TRY = ['utf-8', 'latin-1', 'cp1252']
```

### Step 2: Utility Functions

Create `utils.py`:
```python
import chardet
import pandas as pd
from pathlib import Path
from typing import Optional
import logging

def detect_encoding(file_path: Path) -> str:
    """Detect file encoding"""
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding']

def read_csv_flexible(file_path: Path, encodings: list) -> Optional[pd.DataFrame]:
    """Try reading CSV with multiple encodings"""
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            logging.info(f"Successfully read {file_path.name} with {encoding}")
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue

    logging.error(f"Could not read {file_path} with any encoding")
    return None

def ensure_directory(path: Path):
    """Create directory if it doesn't exist"""
    path.mkdir(parents=True, exist_ok=True)
```

### Step 3: Validation

Create `validator.py`:
```python
import pandas as pd
import logging
from typing import List, Tuple

def validate_dataframe(
    df: pd.DataFrame,
    required_columns: List[str],
    name: str = "DataFrame"
) -> Tuple[bool, List[str]]:
    """
    Validate DataFrame has required columns and is not empty.

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []

    # Check not empty
    if len(df) == 0:
        errors.append(f"{name} is empty")

    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        errors.append(f"{name} missing columns: {missing_cols}")

    # Check for duplicate columns
    if len(df.columns) != len(set(df.columns)):
        duplicates = [col for col in df.columns if list(df.columns).count(col) > 1]
        errors.append(f"{name} has duplicate columns: {set(duplicates)}")

    is_valid = len(errors) == 0

    if is_valid:
        logging.info(f"{name} validation passed: {len(df)} rows, {len(df.columns)} columns")
    else:
        for error in errors:
            logging.error(error)

    return is_valid, errors
```

### Step 4: Main Processor

Create `processor.py`:
```python
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import config
from validator import validate_dataframe
from utils import read_csv_flexible, ensure_directory

class SalesDataProcessor:
    """Main CSV data processor"""

    def __init__(self):
        self.sales_data = None
        self.products = None
        self.customers = None
        self.stats = {
            'files_processed': 0,
            'files_failed': 0,
            'total_records': 0,
            'valid_records': 0,
            'errors': []
        }

    def load_sales_files(self) -> bool:
        """Load and combine all sales CSV files"""
        logging.info("Loading sales files...")

        sales_files = list(config.SALES_DIR.glob('*.csv'))
        if not sales_files:
            logging.error(f"No CSV files found in {config.SALES_DIR}")
            return False

        logging.info(f"Found {len(sales_files)} sales files")

        dfs = []
        for file_path in sales_files:
            try:
                df = read_csv_flexible(file_path, config.ENCODINGS_TO_TRY)
                if df is None:
                    self.stats['files_failed'] += 1
                    continue

                # Validate
                is_valid, errors = validate_dataframe(
                    df,
                    config.SALES_REQUIRED_COLS,
                    file_path.name
                )

                if not is_valid:
                    self.stats['files_failed'] += 1
                    self.stats['errors'].extend(errors)
                    continue

                # Add source tracking
                df['source_file'] = file_path.name

                dfs.append(df)
                self.stats['files_processed'] += 1

            except Exception as e:
                logging.error(f"Error processing {file_path.name}: {e}")
                self.stats['files_failed'] += 1
                self.stats['errors'].append(str(e))

        if not dfs:
            logging.error("No valid sales files loaded")
            return False

        # Combine all sales data
        self.sales_data = pd.concat(dfs, ignore_index=True)
        self.stats['total_records'] = len(self.sales_data)

        logging.info(f"Loaded {self.stats['total_records']} total sales records")
        return True

    def load_reference_data(self) -> bool:
        """Load products and customers data"""
        logging.info("Loading reference data...")

        # Load products
        self.products = read_csv_flexible(config.PRODUCTS_FILE, config.ENCODINGS_TO_TRY)
        if self.products is None:
            return False

        is_valid, errors = validate_dataframe(
            self.products,
            config.PRODUCTS_REQUIRED_COLS,
            "Products"
        )
        if not is_valid:
            return False

        # Load customers
        self.customers = read_csv_flexible(config.CUSTOMERS_FILE, config.ENCODINGS_TO_TRY)
        if self.customers is None:
            return False

        is_valid, errors = validate_dataframe(
            self.customers,
            config.CUSTOMERS_REQUIRED_COLS,
            "Customers"
        )
        if not is_valid:
            return False

        return True

    def enrich_data(self):
        """Merge sales with products and customers"""
        logging.info("Enriching sales data...")

        # Merge with products
        self.sales_data = pd.merge(
            self.sales_data,
            self.products,
            on='product_id',
            how='left'
        )

        # Check for missing products
        missing_products = self.sales_data['product_name'].isna().sum()
        if missing_products > 0:
            logging.warning(f"{missing_products} orders have missing product information")

        # Merge with customers
        self.sales_data = pd.merge(
            self.sales_data,
            self.customers,
            on='customer_id',
            how='left'
        )

        # Check for missing customers
        missing_customers = self.sales_data['name'].isna().sum()
        if missing_customers > 0:
            logging.warning(f"{missing_customers} orders have missing customer information")

    def clean_data(self):
        """Clean and transform data"""
        logging.info("Cleaning data...")

        # Convert dates
        self.sales_data['order_date'] = pd.to_datetime(
            self.sales_data['order_date'],
            errors='coerce'
        )
        self.sales_data['join_date'] = pd.to_datetime(
            self.sales_data['join_date'],
            errors='coerce'
        )

        # Convert numeric columns
        numeric_cols = ['quantity', 'unit_price', 'cost']
        for col in numeric_cols:
            self.sales_data[col] = pd.to_numeric(
                self.sales_data[col],
                errors='coerce'
            )

        # Remove records with critical missing data
        before_count = len(self.sales_data)
        self.sales_data = self.sales_data.dropna(
            subset=['order_date', 'quantity', 'unit_price']
        )
        after_count = len(self.sales_data)

        removed = before_count - after_count
        if removed > 0:
            logging.warning(f"Removed {removed} records with critical missing data")

        self.stats['valid_records'] = after_count

    def calculate_metrics(self):
        """Calculate business metrics"""
        logging.info("Calculating metrics...")

        # Revenue
        self.sales_data['revenue'] = (
            self.sales_data['quantity'] * self.sales_data['unit_price']
        )

        # Profit
        self.sales_data['profit'] = (
            self.sales_data['revenue'] -
            (self.sales_data['quantity'] * self.sales_data['cost'])
        )

        # Profit margin
        self.sales_data['profit_margin'] = (
            self.sales_data['profit'] / self.sales_data['revenue']
        ) * 100

        # Days since customer joined
        self.sales_data['days_since_join'] = (
            self.sales_data['order_date'] - self.sales_data['join_date']
        ).dt.days

    def generate_reports(self):
        """Generate summary reports"""
        logging.info("Generating reports...")

        ensure_directory(config.OUTPUT_DIR)

        # Report 1: Detailed transactions
        self.sales_data.to_csv(
            config.OUTPUT_DIR / 'sales_detailed.csv',
            index=False
        )
        logging.info(f"Created sales_detailed.csv ({len(self.sales_data)} rows)")

        # Report 2: Product performance
        product_summary = self.sales_data.groupby('product_name').agg(
            total_revenue=('revenue', 'sum'),
            total_quantity=('quantity', 'sum'),
            avg_order_size=('quantity', 'mean'),
            total_profit=('profit', 'sum'),
            profit_margin=('profit_margin', 'mean'),
            num_orders=('order_id', 'count')
        ).reset_index()

        product_summary = product_summary.sort_values('total_revenue', ascending=False)
        product_summary.to_csv(
            config.OUTPUT_DIR / 'product_summary.csv',
            index=False
        )
        logging.info(f"Created product_summary.csv ({len(product_summary)} rows)")

        # Report 3: Customer analysis
        customer_summary = self.sales_data.groupby('name').agg(
            total_orders=('order_id', 'count'),
            total_revenue=('revenue', 'sum'),
            avg_order_value=('revenue', 'mean'),
            total_items=('quantity', 'sum'),
            customer_city=('city', 'first'),
            customer_country=('country', 'first')
        ).reset_index()

        customer_summary = customer_summary.sort_values('total_revenue', ascending=False)
        customer_summary.to_csv(
            config.OUTPUT_DIR / 'customer_summary.csv',
            index=False
        )
        logging.info(f"Created customer_summary.csv ({len(customer_summary)} rows)")

    def print_summary(self):
        """Print processing summary"""
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Files failed: {self.stats['files_failed']}")
        print(f"Total records loaded: {self.stats['total_records']}")
        print(f"Valid records after cleaning: {self.stats['valid_records']}")
        print(f"Reports generated: 3")
        print(f"Output directory: {config.OUTPUT_DIR}")
        if self.stats['errors']:
            print(f"\nErrors encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:5]:
                print(f"  - {error}")
        print("="*60 + "\n")

    def process(self):
        """Main processing pipeline"""
        try:
            # Load data
            if not self.load_sales_files():
                logging.error("Failed to load sales files")
                return False

            if not self.load_reference_data():
                logging.error("Failed to load reference data")
                return False

            # Process data
            self.enrich_data()
            self.clean_data()
            self.calculate_metrics()

            # Generate outputs
            self.generate_reports()

            # Summary
            self.print_summary()

            logging.info("Processing completed successfully")
            return True

        except Exception as e:
            logging.error(f"Processing failed: {e}", exc_info=True)
            return False
```

### Step 5: Main Entry Point

Create `main.py`:
```python
import logging
from pathlib import Path
from datetime import datetime
from processor import SalesDataProcessor
import config
from utils import ensure_directory

def setup_logging():
    """Configure logging"""
    ensure_directory(config.LOG_DIR)

    log_file = config.LOG_DIR / f"processor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logging.info("="*60)
    logging.info("Sales Data Processor Started")
    logging.info("="*60)

def main():
    """Main entry point"""
    # Setup
    setup_logging()

    # Create processor
    processor = SalesDataProcessor()

    # Run processing
    success = processor.process()

    if success:
        print("\nProcessing completed successfully!")
        print(f"Check {config.OUTPUT_DIR} for reports")
        print(f"Check {config.LOG_DIR} for detailed logs")
    else:
        print("\nProcessing failed. Check logs for details.")

if __name__ == "__main__":
    main()
```

## Exercise: Build the Project

### Task

Implement the complete CSV data processor following the guide above.

### Requirements

1. Create all the files (config.py, utils.py, validator.py, processor.py, main.py)
2. Generate sample input data files
3. Run the processor and verify it generates correct reports
4. Test with edge cases:
   - Missing product/customer references
   - Malformed CSV files
   - Different encodings
   - Missing columns

### Success Criteria

- All three reports are generated correctly
- Logs capture all operations
- Handles errors without crashing
- Validates input data properly
- Produces accurate calculations

### Extensions (Optional)

Add these advanced features:

1. **Command-line interface**: Use argparse for CLI options
2. **Configuration file**: Load settings from YAML/JSON
3. **Data quality report**: Generate statistics on data issues
4. **Visualizations**: Create charts of key metrics
5. **Email notifications**: Send reports via email
6. **Database export**: Write results to SQLite/PostgreSQL
7. **Incremental processing**: Process only new files
8. **Parallel processing**: Use multiprocessing for multiple files

## Key Takeaways

This project demonstrates:
1. **Modular design**: Separation of concerns (validation, utils, processor)
2. **Error handling**: Graceful handling of all edge cases
3. **Logging**: Comprehensive operational visibility
4. **Data validation**: Ensuring data quality
5. **Data transformation**: Enrichment, cleaning, calculation
6. **Report generation**: Creating actionable insights
7. **Professional structure**: Production-ready code organization

## Conclusion

Congratulations! You've completed the Python CSV File Handling course. You now have the skills to:

- Read and write CSV files with both csv module and pandas
- Handle large files efficiently with chunking
- Process complex data transformations
- Merge and aggregate datasets
- Handle errors and edge cases gracefully
- Build production-ready data processing applications

These skills are fundamental for:
- Data engineering
- Data analysis
- ETL pipeline development
- Report automation
- Data integration

Continue practicing by:
- Processing real-world datasets (Kaggle, data.gov)
- Contributing to open-source data projects
- Building automation tools for your own workflows
- Exploring advanced topics (Dask, Vaex, Apache Spark)

Thank you for completing this course!

---

## Additional Resources

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Python csv Module**: https://docs.python.org/3/library/csv.html
- **Real Datasets**: https://www.kaggle.com/datasets
- **Data Engineering**: Designing Data-Intensive Applications (book)
- **Advanced Pandas**: Modern Pandas series by Tom Augspurger
