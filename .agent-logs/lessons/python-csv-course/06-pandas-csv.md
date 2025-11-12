# Lesson 06: Pandas Deep Dive for CSV Operations

## Context & Motivation

Pandas is the industry standard for data analysis in Python. While you've used basic pandas operations, this lesson unlocks its true power. Pandas transforms CSV files from simple text into rich, queryable data structures that support complex operations: multi-column filtering, aggregations, joins, pivots, and statistical analysis.

Think of pandas DataFrames as supercharged spreadsheets with programming capabilities. Everything you can do in Excel - and much more - becomes programmable, repeatable, and scalable. Data scientists use pandas to clean messy datasets, researchers analyze experimental results, and engineers build ETL pipelines. Mastering pandas means wielding one of the most powerful data manipulation tools in existence.

This lesson focuses on practical pandas operations specifically for CSV workflows. You'll learn the patterns data professionals use daily: filtering complex conditions, aggregating across groups, merging datasets, reshaping data, and handling real-world data quality issues.

## DataFrame Fundamentals

### Understanding DataFrame Structure

A DataFrame is a 2D table with labeled rows and columns:

```python
import pandas as pd

# Create from dictionary
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 28],
    'city': ['New York', 'San Francisco', 'Seattle', 'Boston'],
    'salary': [75000, 85000, 95000, 70000]
})

print(df)
#       name  age           city  salary
# 0    Alice   25       New York   75000
# 1      Bob   30  San Francisco   85000
# 2  Charlie   35        Seattle   95000
# 3    David   28         Boston   70000

# Key attributes
print(df.shape)      # (4, 4) - 4 rows, 4 columns
print(df.columns)    # Column names
print(df.index)      # Row indices
print(df.dtypes)     # Data types of each column
```

**DataFrame anatomy:**
- **Index**: Row labels (0, 1, 2, 3 by default)
- **Columns**: Column names ('name', 'age', 'city', 'salary')
- **Values**: The actual data (2D numpy array underneath)

### Selecting Data

Multiple ways to access DataFrame data:

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Select single column (returns Series)
names = df['name']
print(type(names))  # <class 'pandas.core.series.Series'>

# Select multiple columns (returns DataFrame)
subset = df[['name', 'salary']]
print(type(subset))  # <class 'pandas.core.frame.DataFrame'>

# Select rows by index position (iloc)
first_row = df.iloc[0]        # First row
first_three = df.iloc[0:3]    # First 3 rows
last_row = df.iloc[-1]        # Last row

# Select rows by label (loc)
df_indexed = df.set_index('name')
alice_data = df_indexed.loc['Alice']

# Select specific cells
# df.iloc[row_position, column_position]
value = df.iloc[0, 1]  # First row, second column

# df.loc[row_label, column_name]
value = df.loc[0, 'age']  # Row 0, column 'age'
```

**Key distinction:**
- `.iloc[]`: Select by integer position (0, 1, 2...)
- `.loc[]`: Select by label (row index, column name)

## Advanced Filtering

### Boolean Indexing

Filter DataFrames using boolean conditions:

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Simple condition
high_earners = df[df['salary'] > 80000]

# Multiple conditions with & (AND)
young_high_earners = df[(df['age'] < 30) & (df['salary'] > 70000)]

# Multiple conditions with | (OR)
interesting = df[(df['salary'] > 90000) | (df['age'] < 26)]

# NOT condition with ~
not_from_nyc = df[~(df['city'] == 'New York')]

# Using .isin() for multiple values
tech_hubs = df[df['city'].isin(['San Francisco', 'Seattle', 'Austin'])]

# String conditions
names_with_a = df[df['name'].str.startswith('A')]
emails_gmail = df[df['email'].str.contains('gmail')]
```

**Critical syntax rules:**
- Use `&` for AND, `|` for OR, `~` for NOT
- Always wrap each condition in parentheses: `(condition1) & (condition2)`
- Cannot use Python's `and`, `or`, `not` keywords with pandas

### Query Method (SQL-like)

More readable filtering for complex conditions:

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# SQL-like query syntax
result = df.query('salary > 80000 and age < 35')

# Using variables
min_salary = 70000
result = df.query('salary > @min_salary')

# Complex conditions
result = df.query('(salary > 80000 or age < 28) and city == "Boston"')

# String operations
result = df.query('name.str.startswith("A")', engine='python')
```

**Advantages:**
- More readable than boolean indexing
- Closer to SQL syntax
- Can reference variables with `@`

## Data Transformation

### Creating and Modifying Columns

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Add new column from calculation
df['monthly_salary'] = df['salary'] / 12

# Add column based on condition
df['high_earner'] = df['salary'] > 80000  # Boolean column

# Add column with conditional logic
df['salary_category'] = df['salary'].apply(
    lambda x: 'High' if x > 85000 else ('Medium' if x > 70000 else 'Low')
)

# Better approach for complex conditions: np.select
import numpy as np

conditions = [
    df['salary'] > 85000,
    df['salary'] > 70000,
    df['salary'] <= 70000
]
choices = ['High', 'Medium', 'Low']
df['salary_category'] = np.select(conditions, choices, default='Unknown')

# Modify existing column
df['age'] = df['age'] + 1  # Everyone gets a year older
df['name'] = df['name'].str.upper()  # Uppercase all names

# Multiple columns at once
df[['first_name', 'last_name']] = df['name'].str.split(' ', expand=True)
```

### Apply Functions to Rows

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Apply function to each element in a column
df['salary_formatted'] = df['salary'].apply(lambda x: f"${x:,.2f}")

# Apply function across multiple columns (axis=1 for rows)
def calculate_bonus(row):
    if row['age'] < 30:
        return row['salary'] * 0.10
    elif row['age'] < 40:
        return row['salary'] * 0.15
    else:
        return row['salary'] * 0.20

df['bonus'] = df.apply(calculate_bonus, axis=1)

# More efficient: vectorized operations
# Instead of apply(), use pandas operations when possible
df['bonus'] = np.where(
    df['age'] < 30,
    df['salary'] * 0.10,
    np.where(df['age'] < 40, df['salary'] * 0.15, df['salary'] * 0.20)
)
```

**Performance tip**: Vectorized operations (numpy, pandas operations) are 10-100x faster than `.apply()`.

## Aggregation and Grouping

### Basic Aggregation

```python
import pandas as pd

df = pd.read_csv('sales.csv')

# Single aggregation functions
total_sales = df['amount'].sum()
avg_price = df['price'].mean()
max_quantity = df['quantity'].max()
min_quantity = df['quantity'].min()
count_orders = df['order_id'].count()

# Multiple aggregations at once
summary = df['amount'].agg(['sum', 'mean', 'min', 'max', 'count'])
print(summary)
# sum      125000.50
# mean       2500.01
# min         100.00
# max       10000.00
# count        50.00

# Aggregations across multiple columns
summary = df[['amount', 'quantity']].agg(['sum', 'mean', 'std'])
print(summary)
#           amount   quantity
# sum    125000.50     1500.0
# mean     2500.01       30.0
# std       1234.56       12.5
```

### GroupBy Operations

Group data and compute aggregates per group:

```python
import pandas as pd

df = pd.read_csv('sales.csv')

# Group by single column
by_product = df.groupby('product')['amount'].sum()
print(by_product)
# product
# Laptop      50000
# Mouse        5000
# Keyboard    10000

# Group by multiple columns
by_product_city = df.groupby(['product', 'city'])['amount'].sum()

# Multiple aggregations
sales_summary = df.groupby('product').agg({
    'amount': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'order_id': 'count'
})

# Rename aggregated columns for clarity
sales_summary = df.groupby('product').agg(
    total_sales=('amount', 'sum'),
    avg_sale=('amount', 'mean'),
    num_orders=('order_id', 'count'),
    total_quantity=('quantity', 'sum')
).reset_index()

print(sales_summary)
#    product  total_sales  avg_sale  num_orders  total_quantity
# 0   Laptop      50000.0   1666.67          30            45
# 1    Mouse       5000.0    100.00          50            200
# 2 Keyboard      10000.0    250.00          40            80
```

### Custom Aggregation Functions

```python
import pandas as pd
import numpy as np

df = pd.read_csv('sales.csv')

# Custom function for aggregation
def price_range(series):
    return series.max() - series.min()

summary = df.groupby('product')['price'].agg([
    ('min_price', 'min'),
    ('max_price', 'max'),
    ('price_range', price_range),
    ('avg_price', 'mean')
])

print(summary)
```

## Merging and Joining DataFrames

### Inner Join

Combine DataFrames based on common columns:

```python
import pandas as pd

# Load two CSV files
orders = pd.read_csv('orders.csv')
# order_id, customer_id, amount, date

customers = pd.read_csv('customers.csv')
# customer_id, name, email, city

# Inner join: keep only matching rows
merged = pd.merge(orders, customers, on='customer_id', how='inner')

print(merged.head())
#   order_id  customer_id  amount       date     name            email       city
# 0      1001          501  250.00 2024-01-15    Alice  alice@email.com  New York
# 1      1002          502  150.00 2024-01-16      Bob    bob@email.com   Boston
```

**How it works:**
- Finds rows where `customer_id` matches in both DataFrames
- Combines columns from both
- Only keeps rows with matches in both tables

### Different Join Types

```python
import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')

# Inner join (default): only matching rows
inner = pd.merge(orders, customers, on='customer_id', how='inner')

# Left join: all rows from left (orders), matching from right
left = pd.merge(orders, customers, on='customer_id', how='left')
# If order has customer_id not in customers, customer columns are NaN

# Right join: all rows from right (customers), matching from left
right = pd.merge(orders, customers, on='customer_id', how='right')
# If customer has no orders, order columns are NaN

# Outer join: all rows from both, filling NaN where no match
outer = pd.merge(orders, customers, on='customer_id', how='outer')
```

**Join types visualized:**
- **Inner**: Intersection (only matches)
- **Left**: Left table + matches from right
- **Right**: Right table + matches from left
- **Outer**: Union (everything from both)

### Merging on Different Column Names

```python
import pandas as pd

orders = pd.read_csv('orders.csv')      # has 'cust_id'
customers = pd.read_csv('customers.csv') # has 'id'

# Specify different column names
merged = pd.merge(
    orders,
    customers,
    left_on='cust_id',
    right_on='id',
    how='inner'
)

# Result has both cust_id and id columns (usually want to drop one)
merged = merged.drop('id', axis=1)
```

### Merging on Multiple Columns

```python
import pandas as pd

sales = pd.read_csv('sales.csv')
# date, store_id, product_id, quantity

inventory = pd.read_csv('inventory.csv')
# date, store_id, product_id, stock

# Merge on multiple columns
merged = pd.merge(
    sales,
    inventory,
    on=['date', 'store_id', 'product_id'],
    how='left'
)
```

### Concatenating DataFrames

Combine DataFrames vertically or horizontally:

```python
import pandas as pd

# Read multiple CSV files
df1 = pd.read_csv('sales_january.csv')
df2 = pd.read_csv('sales_february.csv')
df3 = pd.read_csv('sales_march.csv')

# Concatenate vertically (stack rows)
all_sales = pd.concat([df1, df2, df3], ignore_index=True)

# Add a source column to track origin
df1['month'] = 'January'
df2['month'] = 'February'
df3['month'] = 'March'
all_sales = pd.concat([df1, df2, df3], ignore_index=True)

# Concatenate horizontally (add columns)
df_left = pd.read_csv('data_part1.csv')
df_right = pd.read_csv('data_part2.csv')
combined = pd.concat([df_left, df_right], axis=1)
```

## Data Cleaning

### Handling Missing Values

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Detect missing values
print(df.isnull().sum())  # Count of NaN per column
print(df.isna().sum())     # Same as isnull()

# Drop rows with any missing values
df_clean = df.dropna()

# Drop rows where specific column is missing
df_clean = df.dropna(subset=['email'])

# Fill missing values with a constant
df_filled = df.fillna(0)
df_filled = df.fillna({'age': 0, 'city': 'Unknown'})

# Fill with forward/backward values
df_filled = df.fillna(method='ffill')  # Forward fill
df_filled = df.fillna(method='bfill')  # Backward fill

# Fill with column mean/median
df['age'].fillna(df['age'].mean(), inplace=True)
df['salary'].fillna(df['salary'].median(), inplace=True)

# Replace specific values
df.replace({'city': {'NYC': 'New York', 'SF': 'San Francisco'}}, inplace=True)
```

### Removing Duplicates

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Find duplicates
duplicates = df.duplicated()
print(f"Number of duplicates: {duplicates.sum()}")

# Remove exact duplicate rows
df_unique = df.drop_duplicates()

# Remove duplicates based on specific columns
df_unique = df.drop_duplicates(subset=['email'])

# Keep last occurrence instead of first
df_unique = df.drop_duplicates(subset=['email'], keep='last')

# Mark duplicates but don't remove
df['is_duplicate'] = df.duplicated(subset=['email'])
```

### Data Type Conversion

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Convert column to different type
df['age'] = df['age'].astype(int)
df['price'] = df['price'].astype(float)
df['category'] = df['category'].astype('category')  # Categorical type

# Convert string to datetime
df['date'] = pd.to_datetime(df['date'])

# Handle errors in conversion
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Invalid → NaN

# Convert multiple columns
df[['col1', 'col2']] = df[['col1', 'col2']].astype(float)
```

## Interactive Exercises

### Exercise 1 [Intermediate]: Complex Filtering

**Goal**: Master multi-condition filtering

**Task**: Create or load an employees CSV with: name, age, department, salary, years_experience. Write a script that finds employees who:
- Are in Engineering or Sales departments, AND
- Have salary > 70000 OR years_experience > 5, AND
- Are not older than 40

**Success Criteria**:
- Uses pandas boolean indexing
- All three condition groups apply correctly
- Results are saved to new CSV

**Hint**: Use parentheses carefully: `((cond1 | cond2) & cond3 & cond4)`

### Exercise 2 [Intermediate]: GroupBy Analysis

**Goal**: Perform multi-level aggregation

**Task**: Create a sales CSV with: date, product, category, region, quantity, price. Calculate:
1. Total revenue per category (quantity × price)
2. Average sale amount per region
3. Top 3 products by total quantity sold
4. Number of sales per category per region

**Success Criteria**:
- Uses groupby effectively
- Multiple aggregation functions applied
- Results are organized and readable
- Each analysis saved to separate CSV

**Hint**: Use `.agg()` with dictionary to specify different functions for different columns

### Exercise 3 [Advanced]: Merge Multiple DataFrames

**Goal**: Master joining operations

**Task**: You have three CSV files:
- `orders.csv`: order_id, customer_id, product_id, quantity, order_date
- `customers.csv`: customer_id, name, email, city
- `products.csv`: product_id, product_name, category, price

Create a complete orders report that includes customer and product information.

**Success Criteria**:
- Performs two merges correctly
- Adds calculated column: total = quantity × price
- Handles missing matches appropriately
- Exports enriched dataset

**Hint**: Merge orders with customers first, then merge result with products

### Exercise 4 [Advanced]: Data Cleaning Pipeline

**Goal**: Build comprehensive cleaning workflow

**Task**: Create a "dirty" CSV with intentional issues:
- Missing values in various columns
- Duplicate rows
- Inconsistent formatting (e.g., "NYC", "New York", "new york")
- Wrong data types (dates as strings)

Write a cleaning script that:
1. Reports initial data quality issues
2. Handles missing values appropriately
3. Removes duplicates
4. Standardizes values
5. Converts types correctly
6. Exports clean data

**Success Criteria**:
- Addresses all data quality issues
- Provides before/after statistics
- Clean data is ready for analysis
- Script is well-documented

**Hint**: Handle issues in order: types → missing → duplicates → standardization

### Exercise 5 [Expert]: Sales Analysis Dashboard Data

**Goal**: Create analysis-ready dataset from multiple sources

**Task**: Build a comprehensive sales analysis dataset:
1. Load monthly sales CSVs (3-4 files)
2. Load customer and product reference data
3. Merge all datasets
4. Add calculated columns: revenue, profit_margin, customer_lifetime_value
5. Create aggregated views: by month, by product, by customer
6. Export 3 CSVs: detailed transactions, monthly summary, product summary

**Success Criteria**:
- Handles multiple file concatenation
- Performs accurate merges
- Calculations are correct
- Produces three well-structured output files
- Code is organized and efficient

**Hint**: Start with concatenating monthly files, then merge reference data, then calculate, then aggregate

## Quick Reference: Common Pandas Patterns

### Pattern 1: Read, Filter, Save
```python
df = pd.read_csv('in.csv')
df_filtered = df[df['col'] > threshold]
df_filtered.to_csv('out.csv', index=False)
```

### Pattern 2: GroupBy and Aggregate
```python
summary = df.groupby('category').agg({
    'amount': 'sum',
    'quantity': 'mean'
}).reset_index()
```

### Pattern 3: Merge Two DataFrames
```python
merged = pd.merge(df1, df2, on='id', how='inner')
```

### Pattern 4: Add Calculated Column
```python
df['new_col'] = df['col1'] * df['col2']
```

### Pattern 5: Complex Boolean Filter
```python
result = df[(df['a'] > 10) & (df['b'].isin(['x', 'y'])) | (df['c'] < 5)]
```

## Key Takeaways

1. **Boolean indexing is powerful** - Master the syntax for complex filters
2. **GroupBy enables insights** - Aggregate data by categories
3. **Merging combines datasets** - Understand join types
4. **Vectorized operations are fast** - Avoid .apply() when possible
5. **Clean data first** - Handle missing values and duplicates early
6. **DataFrames are flexible** - Add, remove, transform columns easily
7. **Read pandas docs** - Extensive functionality beyond this lesson

## Looking Ahead

You now have professional-level pandas skills for CSV operations. Next, you'll learn error handling, encoding issues, and best practices to make your CSV processing robust and production-ready.

**Next Lesson**: [07 - Error Handling & Best Practices](07-best-practices.md)

---

## Further Exploration

- **Pandas query optimization**: Using eval() for large DataFrames
- **Categorical data**: Memory-efficient representation
- **Time series**: DateTimeIndex and resampling
- **Styling**: Formatting DataFrames for reports
- **Integration**: SQLAlchemy for database operations
