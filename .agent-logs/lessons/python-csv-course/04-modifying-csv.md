# Lesson 04: Modifying CSV Files

## Context & Motivation

In the real world, CSV files rarely stay static. You'll constantly need to update values, add new columns, filter rows, or transform data based on business logic. Maybe you need to apply a price increase to all products, add calculated fields, remove outdated records, or merge information from multiple sources.

Modifying CSV files is where reading and writing skills converge. The pattern is always the same: read data → transform it → write it back. However, the devil is in the details. How do you efficiently update specific rows without loading everything into memory? How do you add a column while preserving existing data? How do you safely overwrite files without losing data if something goes wrong?

Understanding CSV modification unlocks powerful data processing workflows. You'll build tools that clean datasets, apply business rules, enrich data with calculations, and maintain data quality - all essential skills for data engineering and automation.

## The Core Pattern: Read → Transform → Write

Every CSV modification follows this three-step pattern:

```python
# STEP 1: Read the data
data = read_from_csv()

# STEP 2: Transform the data
modified_data = transform(data)

# STEP 3: Write it back
write_to_csv(modified_data)
```

Let's explore different ways to implement this pattern.

## Basic Modification with csv Module

### Updating Specific Values

Let's say you have a products CSV and need to increase all prices by 10%:

```python
import csv

# Read the original file
rows = []
with open('products.csv', 'r') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Transform: increase price by 10%
        old_price = float(row['price'])
        new_price = old_price * 1.10
        row['price'] = f"{new_price:.2f}"  # Format to 2 decimal places

        rows.append(row)

# Write back to the same file (or a new file)
with open('products_updated.csv', 'w', newline='') as file:
    # Get fieldnames from first row
    fieldnames = rows[0].keys()

    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(rows)

print("Prices updated successfully!")
```

**What's happening:**
1. Read all rows into memory as dictionaries
2. Modify the 'price' field in each row
3. Write all modified rows to a new file
4. Use DictReader/DictWriter for easy field access

**Important**: This loads the entire file into memory. Fine for small to medium files (<100K rows).

### In-Place Modification Pattern

To overwrite the original file safely:

```python
import csv
import os

input_file = 'products.csv'
temp_file = 'products_temp.csv'

# Read and write to temporary file
with open(input_file, 'r') as infile, open(temp_file, 'w', newline='') as outfile:
    csv_reader = csv.DictReader(infile)

    fieldnames = csv_reader.fieldnames
    csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    csv_writer.writeheader()

    for row in csv_reader:
        # Modify the row
        row['price'] = str(float(row['price']) * 1.10)
        csv_writer.writerow(row)

# Replace original with modified file
os.replace(temp_file, input_file)

print("File updated in-place!")
```

**Why use a temporary file?**
- If an error occurs during writing, your original file is safe
- `os.replace()` is atomic on most systems - no data corruption
- Professional approach to file modification

### Filtering Rows

Remove rows that don't meet certain criteria:

```python
import csv

# Read and filter
filtered_rows = []
with open('employees.csv', 'r') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Only keep employees with salary >= 50000
        if float(row['salary']) >= 50000:
            filtered_rows.append(row)

# Write filtered data
with open('high_salary_employees.csv', 'w', newline='') as file:
    fieldnames = filtered_rows[0].keys()
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(filtered_rows)

print(f"Filtered: {len(filtered_rows)} employees kept")
```

### Adding New Columns

Add calculated or derived columns:

```python
import csv

# Read data
rows = []
with open('sales.csv', 'r') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Add new column: total = quantity * price
        quantity = int(row['quantity'])
        price = float(row['price'])
        row['total'] = f"{quantity * price:.2f}"

        rows.append(row)

# Write with new column
with open('sales_with_total.csv', 'w', newline='') as file:
    # Add 'total' to fieldnames
    fieldnames = list(rows[0].keys())

    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(rows)

print("New column added!")
```

**Key insight**: When using DictReader, you can simply add new keys to the dictionary. When writing, include those new keys in fieldnames.

### Removing Columns

Keep only specific columns:

```python
import csv

# Columns to keep
columns_to_keep = ['name', 'email', 'phone']

# Read and select columns
rows = []
with open('contacts.csv', 'r') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Create new dict with only desired columns
        filtered_row = {col: row[col] for col in columns_to_keep}
        rows.append(filtered_row)

# Write with selected columns only
with open('contacts_minimal.csv', 'w', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=columns_to_keep)
    csv_writer.writeheader()
    csv_writer.writerows(rows)

print("Columns removed!")
```

## Efficient Modification with Pandas

Pandas makes CSV modification dramatically simpler and more powerful.

### Basic Value Updates

```python
import pandas as pd

# Read CSV
df = pd.read_csv('products.csv')

# Update values: increase all prices by 10%
df['price'] = df['price'] * 1.10

# Write back
df.to_csv('products_updated.csv', index=False)

print("Prices updated!")
```

**That's it!** Three lines of actual logic. Pandas handles all the CSV parsing and writing.

### Conditional Updates

Update only rows meeting specific criteria:

```python
import pandas as pd

df = pd.read_csv('employees.csv')

# Give 10% raise to employees with salary < 60000
df.loc[df['salary'] < 60000, 'salary'] *= 1.10

# Or using a more explicit approach
mask = df['salary'] < 60000
df.loc[mask, 'salary'] = df.loc[mask, 'salary'] * 1.10

df.to_csv('employees_updated.csv', index=False)
```

**How this works:**
- `df['salary'] < 60000`: Creates a boolean mask (True/False for each row)
- `df.loc[mask, 'salary']`: Selects rows where mask is True, 'salary' column
- `*= 1.10`: Multiplies those values by 1.10

### Adding Calculated Columns

```python
import pandas as pd

df = pd.read_csv('sales.csv')

# Add total column
df['total'] = df['quantity'] * df['price']

# Add discount column (10% if quantity > 10)
df['discount'] = df['quantity'].apply(lambda x: 0.10 if x > 10 else 0.0)

# Add final_price after discount
df['final_price'] = df['total'] * (1 - df['discount'])

df.to_csv('sales_enhanced.csv', index=False)
```

**Pandas power:**
- Vectorized operations: `df['quantity'] * df['price']` multiplies entire columns at once
- `.apply()`: Apply custom logic to each value
- Multiple operations in sequence

### Filtering Rows

```python
import pandas as pd

df = pd.read_csv('students.csv')

# Keep only students with GPA >= 3.5
df_filtered = df[df['gpa'] >= 3.5]

# Multiple conditions: GPA >= 3.5 AND grade == 12
df_filtered = df[(df['gpa'] >= 3.5) & (df['grade'] == 12)]

# Or condition: GPA >= 3.8 OR perfect attendance
df_filtered = df[(df['gpa'] >= 3.8) | (df['attendance'] == 100)]

df_filtered.to_csv('honor_students.csv', index=False)

print(f"Kept {len(df_filtered)} out of {len(df)} students")
```

**Boolean indexing:**
- `&`: AND operator
- `|`: OR operator
- `~`: NOT operator
- Always use parentheses around each condition!

### Removing and Reordering Columns

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Remove columns
df_cleaned = df.drop(['unnecessary_col1', 'temporary_col'], axis=1)

# Keep only specific columns
df_minimal = df[['name', 'email', 'phone']]

# Reorder columns
column_order = ['id', 'name', 'email', 'phone', 'city']
df_reordered = df[column_order]

df_reordered.to_csv('data_cleaned.csv', index=False)
```

### Renaming Columns

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Rename specific columns
df_renamed = df.rename(columns={
    'old_name': 'new_name',
    'col1': 'column_one',
    'col2': 'column_two'
})

# Or rename all columns at once
df.columns = ['id', 'name', 'age', 'city']

df_renamed.to_csv('data_renamed.csv', index=False)
```

### Updating Based on Another Column

```python
import pandas as pd

df = pd.read_csv('products.csv')

# Different price increase based on category
def calculate_new_price(row):
    if row['category'] == 'Electronics':
        return row['price'] * 1.15  # 15% increase
    elif row['category'] == 'Clothing':
        return row['price'] * 1.10  # 10% increase
    else:
        return row['price'] * 1.05  # 5% increase

df['new_price'] = df.apply(calculate_new_price, axis=1)

df.to_csv('products_updated.csv', index=False)
```

**Understanding `.apply()`:**
- `axis=1`: Apply function to each row
- Function receives entire row as parameter
- Can access multiple columns in the logic
- Returns the new value

## Advanced Modification Techniques

### Handling Missing Values During Modification

```python
import pandas as pd

df = pd.read_csv('data.csv')

# Fill missing values with defaults
df['age'].fillna(0, inplace=True)
df['city'].fillna('Unknown', inplace=True)

# Or drop rows with missing values
df_cleaned = df.dropna()

# Drop rows where specific column is missing
df_cleaned = df.dropna(subset=['email'])

df_cleaned.to_csv('data_cleaned.csv', index=False)
```

### Aggregating and Summarizing

Create summary CSV from detailed data:

```python
import pandas as pd

df = pd.read_csv('sales.csv')

# Group by product and sum quantities
summary = df.groupby('product')['quantity'].sum().reset_index()
summary.columns = ['product', 'total_quantity']

# Multiple aggregations
summary = df.groupby('product').agg({
    'quantity': 'sum',
    'price': 'mean',
    'order_id': 'count'
}).reset_index()

summary.columns = ['product', 'total_quantity', 'avg_price', 'num_orders']

summary.to_csv('sales_summary.csv', index=False)
```

### Sorting Data

```python
import pandas as pd

df = pd.read_csv('students.csv')

# Sort by single column
df_sorted = df.sort_values('gpa', ascending=False)  # Highest GPA first

# Sort by multiple columns
df_sorted = df.sort_values(['grade', 'gpa'], ascending=[True, False])
# First by grade (ascending), then by GPA (descending) within each grade

df_sorted.to_csv('students_sorted.csv', index=False)
```

### Deduplicating Data

```python
import pandas as pd

df = pd.read_csv('contacts.csv')

# Remove exact duplicate rows
df_unique = df.drop_duplicates()

# Remove duplicates based on specific column(s)
df_unique = df.drop_duplicates(subset=['email'])

# Keep last occurrence instead of first
df_unique = df.drop_duplicates(subset=['email'], keep='last')

df_unique.to_csv('contacts_unique.csv', index=False)

print(f"Removed {len(df) - len(df_unique)} duplicates")
```

## Memory-Efficient Modification for Large Files

When files are too large for memory:

```python
import csv

input_file = 'large_data.csv'
output_file = 'large_data_modified.csv'

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    csv_reader = csv.DictReader(infile)

    # Get fieldnames and possibly add new ones
    fieldnames = list(csv_reader.fieldnames) + ['new_column']

    csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    csv_writer.writeheader()

    # Process one row at a time
    for row in csv_reader:
        # Modify row
        row['price'] = str(float(row['price']) * 1.10)
        row['new_column'] = 'calculated_value'

        # Write immediately
        csv_writer.writerow(row)

print("Large file processed efficiently!")
```

**Key advantage**: Memory usage stays constant regardless of file size.

## Interactive Exercises

### Exercise 1 [Beginner]: Price Update

**Goal**: Practice basic CSV modification

**Task**: Create a CSV file with product data: name, price, stock. Write a script that:
1. Reads the CSV
2. Increases all prices by 15%
3. Writes to a new file called `products_increased.csv`

Use the `csv` module for this exercise.

**Success Criteria**:
- All prices are increased correctly (15%)
- Original file is unchanged
- New file is properly formatted with headers

**Hint**: Use DictReader to read, modify the 'price' field, then use DictWriter to write

### Exercise 2 [Beginner]: Column Addition with Pandas

**Goal**: Learn to add calculated columns with pandas

**Task**: Create a CSV with: product, quantity, unit_price. Use pandas to:
1. Add a `total_price` column (quantity × unit_price)
2. Add a `tax` column (8% of total_price)
3. Add a `final_price` column (total_price + tax)
4. Save the result

**Success Criteria**:
- All three new columns are added
- Calculations are correct
- Uses pandas DataFrame

**Hint**: Chain the column additions: `df['total'] = ...; df['tax'] = ...; df['final'] = ...`

### Exercise 3 [Intermediate]: Conditional Update

**Goal**: Master conditional updates with pandas

**Task**: Create a students CSV with: name, grade, gpa, attendance. Write a script that:
1. Gives +0.1 GPA bonus to students with attendance >= 95%
2. But caps GPA at 4.0 (don't exceed)
3. Filters to keep only students with GPA >= 3.0
4. Saves the result

**Success Criteria**:
- Bonus applied correctly based on attendance
- GPA never exceeds 4.0
- Only students with GPA >= 3.0 remain
- Uses pandas conditional operations

**Hint**: Use `df.loc[condition, column]` for conditional updates, then `df.clip(upper=4.0)` to cap values

### Exercise 4 [Intermediate]: Multi-Step Transformation

**Goal**: Chain multiple modifications

**Task**: Create an orders CSV with: order_id, customer, product, quantity, price, date. Transform it by:
1. Adding `total` column (quantity × price)
2. Adding `discount` column (10% if total > 100, else 0%)
3. Adding `final_total` column (total × (1 - discount))
4. Removing the `price` and `quantity` columns
5. Sorting by final_total (descending)
6. Saving only orders with final_total > 50

Use pandas for this exercise.

**Success Criteria**:
- All transformations apply correctly
- Columns are added and removed as specified
- Data is properly sorted and filtered
- Clean final output

**Hint**: Do operations in sequence: add columns → drop columns → sort → filter → save

### Exercise 5 [Advanced]: Safe In-Place Modification

**Goal**: Learn safe file modification patterns

**Task**: Write a robust script that modifies a CSV in-place. The script should:
1. Read `data.csv`
2. Apply some transformation (your choice)
3. Use a temporary file approach
4. Only replace original if writing succeeds
5. Handle errors gracefully (with try-except)
6. Print status messages

**Success Criteria**:
- Uses temporary file pattern
- Original file safe if error occurs
- Proper error handling implemented
- Informative status messages

**Hint**: Use `try-except-finally` block, and `os.replace()` for atomic file replacement

## Quick Reference: Common Modification Patterns

### Pattern 1: Simple Update (csv module)
```python
import csv
rows = []
with open('file.csv', 'r') as f:
    for row in csv.DictReader(f):
        row['field'] = new_value
        rows.append(row)
with open('file_new.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
```

### Pattern 2: Add Column (pandas)
```python
import pandas as pd
df = pd.read_csv('file.csv')
df['new_col'] = df['col1'] * df['col2']
df.to_csv('file_new.csv', index=False)
```

### Pattern 3: Filter Rows (pandas)
```python
import pandas as pd
df = pd.read_csv('file.csv')
df_filtered = df[df['column'] > threshold]
df_filtered.to_csv('file_filtered.csv', index=False)
```

### Pattern 4: In-Place Modification (csv module)
```python
import csv, os
with open('file.csv', 'r') as inf, open('temp.csv', 'w', newline='') as outf:
    reader = csv.DictReader(inf)
    writer = csv.DictWriter(outf, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        row['field'] = modify(row['field'])
        writer.writerow(row)
os.replace('temp.csv', 'file.csv')
```

### Pattern 5: Conditional Update (pandas)
```python
import pandas as pd
df = pd.read_csv('file.csv')
df.loc[df['col'] > 100, 'other_col'] = new_value
df.to_csv('file_new.csv', index=False)
```

## Key Takeaways

1. **Read → Transform → Write** is the universal pattern
2. **Use temporary files** for safe in-place modification
3. **Pandas is powerful** for complex transformations
4. **csv module is efficient** for large files processed row-by-row
5. **Boolean indexing** in pandas enables sophisticated filtering
6. **Always test** on a copy before modifying original files
7. **Vectorized operations** in pandas are faster than loops

## Looking Ahead

You've mastered reading, writing, and modifying CSV files. Next, you'll learn advanced techniques: processing files too large for memory, custom CSV dialects, and optimization strategies for high-performance data processing.

**Next Lesson**: [05 - Advanced CSV Techniques](05-advanced-csv.md)

---

## Further Exploration

- **Atomic operations**: Transaction-like file modifications
- **Backup strategies**: Versioning CSV files before modification
- **Data validation**: Ensuring data quality during modification
- **Parallel processing**: Using multiprocessing for large CSV transformations
