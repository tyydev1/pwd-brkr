# Lesson 03: Writing CSV Files

## Context & Motivation

Reading CSV files is only half the story - you need to write them too. Every time you generate a report, export processed data, create a backup, or share results with others, you're writing CSV files. It's how your program communicates its output to the world.

Writing CSV files is surprisingly more nuanced than reading them. You need to decide: Should I create a new file or append to an existing one? How do I handle special characters in my data? What happens if a field contains commas or newlines? Should I write from lists or dictionaries? These questions matter because CSV files you create need to be readable by other systems, from Excel to databases to web applications.

Python gives you precise control over CSV writing through both the `csv` module and pandas. Mastering both approaches means you can generate perfectly formatted CSV files for any situation - whether it's a simple export or a complex data transformation pipeline.

## Writing CSV with Python's `csv` Module

### How CSV Writing Works

The `csv` module handles all the tricky parts of CSV formatting: escaping special characters, adding quotes when needed, ensuring proper line breaks. You provide the data, and it produces properly formatted CSV output. The writer iterates through your data structure and serializes it to text format.

### Basic CSV Writing

Let's start by creating a simple CSV file from scratch:

```python
import csv

# Data as a list of lists
data = [
    ['name', 'age', 'city'],  # Header row
    ['Alice', '25', 'New York'],
    ['Bob', '30', 'San Francisco'],
    ['Charlie', '35', 'Seattle']
]

# Write to CSV file
with open('output.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)

    # Write all rows
    csv_writer.writerows(data)

print("CSV file created successfully!")
```

**Critical details:**
- `open('output.csv', 'w', newline='')`:
  - `'w'`: Write mode (creates new file or overwrites existing)
  - `newline=''`: Essential! Prevents double line breaks on Windows
- `csv.writer(file)`: Creates a writer object
- `writerows(data)`: Writes multiple rows at once

**Result (output.csv):**
```csv
name,age,city
Alice,25,New York
Bob,30,San Francisco
Charlie,35,Seattle
```

### Writing Row by Row

For dynamic data generation or when building data incrementally:

```python
import csv

with open('students.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)

    # Write header
    csv_writer.writerow(['student_id', 'name', 'grade', 'gpa'])

    # Write rows one at a time
    csv_writer.writerow([1001, 'Alice Johnson', 10, 3.8])
    csv_writer.writerow([1002, 'Bob Smith', 11, 3.5])
    csv_writer.writerow([1003, 'Charlie Brown', 10, 3.9])

    # Can write dynamically generated data
    for i in range(1004, 1007):
        csv_writer.writerow([i, f'Student {i}', 12, 3.7])
```

**Key point**: `writerow()` writes one row, `writerows()` writes multiple rows.

### Writing from Dictionaries with DictWriter

When your data is structured as dictionaries, `DictWriter` is cleaner and more maintainable:

```python
import csv

# Data as list of dictionaries
students = [
    {'name': 'Alice', 'age': 15, 'grade': 10, 'gpa': 3.8},
    {'name': 'Bob', 'age': 16, 'grade': 11, 'gpa': 3.5},
    {'name': 'Charlie', 'age': 15, 'grade': 10, 'gpa': 3.9}
]

with open('students.csv', 'w', newline='') as file:
    # Specify the field names (column order)
    fieldnames = ['name', 'age', 'grade', 'gpa']

    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write header row
    csv_writer.writeheader()

    # Write all dictionary rows
    csv_writer.writerows(students)
```

**Why DictWriter is powerful:**
- Column order defined explicitly in `fieldnames`
- Self-documenting: clear what each value represents
- Resilient to data structure changes
- Works great with JSON data or database query results

### Writing with Different Delimiters

Not everyone uses commas. Customize the delimiter:

```python
import csv

data = [
    ['name', 'age', 'city'],
    ['Alice', '25', 'New York'],
    ['Bob', '30', 'San Francisco']
]

# Tab-separated file
with open('output.tsv', 'w', newline='') as file:
    csv_writer = csv.writer(file, delimiter='\t')
    csv_writer.writerows(data)

# Semicolon-separated file (common in Europe)
with open('output_semicolon.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, delimiter=';')
    csv_writer.writerows(data)

# Pipe-separated file
with open('output.psv', 'w', newline='') as file:
    csv_writer = csv.writer(file, delimiter='|')
    csv_writer.writerows(data)
```

### Appending to Existing Files

Sometimes you want to add data to an existing CSV without overwriting it:

```python
import csv

# New data to append
new_students = [
    ['David', '17', '11'],
    ['Eve', '16', '10']
]

# Open in append mode
with open('students.csv', 'a', newline='') as file:
    csv_writer = csv.writer(file)

    # Write new rows
    csv_writer.writerows(new_students)

print("Data appended successfully!")
```

**Critical difference:**
- `'w'`: Write mode - **erases existing file**
- `'a'`: Append mode - **adds to end of file**

**Important**: When appending, don't write headers again!

### Handling Special Characters

The `csv` module automatically handles special characters:

```python
import csv

# Data with commas, quotes, and newlines
data = [
    ['name', 'description', 'notes'],
    ['Product A', 'Small, lightweight widget', 'Best seller'],
    ['Product B', 'He said "amazing"', 'Customer favorite'],
    ['Product C', 'Multi-line\nDescription here', 'New item']
]

with open('products.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)
```

**Result (products.csv):**
```csv
name,description,notes
Product A,"Small, lightweight widget",Best seller
Product B,"He said ""amazing""",Customer favorite
Product C,"Multi-line
Description here",New item
```

**What happened:**
- Fields with commas: Automatically quoted
- Fields with quotes: Quotes doubled (`""`)
- Multi-line fields: Preserved and quoted
- The `csv` module handles all escaping for you!

### Controlling Quoting Behavior

Fine-tune when fields get quoted:

```python
import csv

data = [['name', 'value'], ['Alice', '100'], ['Bob', '200']]

# Quote all fields
with open('output_all.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    csv_writer.writerows(data)
# Result: "name","value"
#         "Alice","100"

# Quote only non-numeric fields
with open('output_nonnumeric.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerows(data)
# Result: "name","value"
#         "Alice",100

# Quote only fields with special characters (default)
with open('output_minimal.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerows(data)
# Result: name,value
#         Alice,100

# Never quote (dangerous - can break CSV format!)
with open('output_none.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\')
    csv_writer.writerows(data)
```

**Quoting modes:**
- `QUOTE_MINIMAL`: Quote only when necessary (default, recommended)
- `QUOTE_ALL`: Quote every field
- `QUOTE_NONNUMERIC`: Quote all non-numeric fields
- `QUOTE_NONE`: Never quote (requires escapechar)

## Writing CSV with Pandas

### Basic Pandas CSV Writing

Pandas makes writing DataFrames to CSV incredibly simple:

```python
import pandas as pd

# Create a DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['New York', 'San Francisco', 'Seattle']
})

# Write to CSV
df.to_csv('output.csv', index=False)

print("CSV file created!")
```

**Key parameter**: `index=False` - Don't write row indices to the file

**Result (output.csv):**
```csv
name,age,city
Alice,25,New York
Bob,30,San Francisco
Charlie,35,Seattle
```

### Pandas Writing Options

Pandas offers extensive control over CSV output:

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['New York', 'San Francisco', 'Seattle'],
    'salary': [75000, 85000, 95000]
})

# Write without headers
df.to_csv('no_header.csv', header=False, index=False)

# Write only specific columns
df.to_csv('names_ages.csv', columns=['name', 'age'], index=False)

# Use different delimiter
df.to_csv('output.tsv', sep='\t', index=False)

# Append to existing file
df.to_csv('output.csv', mode='a', header=False, index=False)

# Specify encoding
df.to_csv('output_utf8.csv', encoding='utf-8', index=False)

# Control floating point precision
df_floats = pd.DataFrame({'value': [3.14159265, 2.71828182]})
df_floats.to_csv('precise.csv', float_format='%.2f', index=False)
# Result: value
#         3.14
#         2.72

# Handle missing values
df_with_na = pd.DataFrame({'a': [1, None, 3], 'b': [4, 5, None]})
df_with_na.to_csv('with_na.csv', na_rep='NULL', index=False)
# Result: a,b
#         1,4
#         NULL,5
#         3,NULL
```

### Writing from Different Data Sources

Pandas can write from various data structures:

```python
import pandas as pd

# From a dictionary
data_dict = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'score': [95, 87, 92]
}
df = pd.DataFrame(data_dict)
df.to_csv('from_dict.csv', index=False)

# From a list of lists
data_list = [
    ['Alice', 95],
    ['Bob', 87],
    ['Charlie', 92]
]
df = pd.DataFrame(data_list, columns=['name', 'score'])
df.to_csv('from_list.csv', index=False)

# From a list of dictionaries
data_dicts = [
    {'name': 'Alice', 'score': 95},
    {'name': 'Bob', 'score': 87},
    {'name': 'Charlie', 'score': 92}
]
df = pd.DataFrame(data_dicts)
df.to_csv('from_dicts.csv', index=False)
```

### Writing Large DataFrames Efficiently

For large datasets, optimize the writing process:

```python
import pandas as pd
import numpy as np

# Create a large DataFrame
large_df = pd.DataFrame({
    'id': range(1000000),
    'value': np.random.randn(1000000),
    'category': np.random.choice(['A', 'B', 'C'], 1000000)
})

# Write with compression
large_df.to_csv('large_data.csv.gz', compression='gzip', index=False)

# Write in chunks (for streaming scenarios)
# This is more relevant when processing data in chunks
# and writing progressively
```

## Comparison: csv Module vs Pandas Writing

| Feature | csv Module | Pandas |
|---------|-----------|--------|
| **Syntax** | More verbose | Very concise |
| **Data Source** | Lists, dicts | DataFrames |
| **Memory** | Efficient | Higher overhead |
| **Control** | Fine-grained | High-level options |
| **Type Handling** | Manual | Automatic |
| **Best For** | Simple exports, streaming | Data analysis pipelines |

## Interactive Exercises

### Exercise 1 [Beginner]: Generate Contact List

**Goal**: Practice basic CSV writing with csv module

**Task**: Create a Python script that generates a CSV file named `contacts.csv` with columns: name, email, phone. Add at least 5 contacts. Use the `csv.writer()` approach.

**Success Criteria**:
- CSV file is created successfully
- All 5 contacts are present
- File can be opened in Excel/spreadsheet software
- Headers are included

**Hint**: Remember to use `newline=''` when opening the file for writing

### Exercise 2 [Beginner]: Dictionary to CSV

**Goal**: Learn DictWriter usage

**Task**: You have this list of dictionaries representing books:
```python
books = [
    {'title': 'The Hobbit', 'author': 'Tolkien', 'year': 1937, 'pages': 310},
    {'title': '1984', 'author': 'Orwell', 'year': 1949, 'pages': 328},
    {'title': 'Dune', 'author': 'Herbert', 'year': 1965, 'pages': 688}
]
```
Write this to a CSV file using `DictWriter`.

**Success Criteria**:
- Uses DictWriter (not regular writer)
- Header row is included
- All books are written correctly
- Column order matches: title, author, year, pages

**Hint**: Use `writeheader()` to automatically write column names

### Exercise 3 [Intermediate]: Data Transformation and Export

**Goal**: Practice reading, transforming, and writing

**Task**: Create a CSV file with product data: product_name, price, quantity. Write a script that:
1. Reads the CSV
2. Adds a new column `total_value` (price × quantity)
3. Writes the result to a new CSV file

Use the `csv` module for this exercise.

**Success Criteria**:
- Reads original CSV correctly
- Calculates total_value accurately
- Writes new CSV with the additional column
- Preserves all original data

**Hint**: Use DictReader to read, calculate the new field, then use DictWriter with updated fieldnames

### Exercise 4 [Intermediate]: Pandas Report Generation

**Goal**: Master pandas CSV export with formatting

**Task**: Create a sales report using pandas. Generate random sales data (use `numpy.random` or manual data) with columns: date, product, quantity, price. Then:
1. Calculate total_sales (quantity × price)
2. Write to CSV with 2 decimal places for price and total_sales
3. Sort by date before writing
4. Don't include the index

**Success Criteria**:
- Uses pandas DataFrame
- Proper numeric formatting
- Data is sorted
- Clean CSV output without index column

**Hint**: Use `sort_values()` before `to_csv()`, and `float_format` parameter

### Exercise 5 [Advanced]: Append with Validation

**Goal**: Learn safe appending to CSV files

**Task**: Write a script that appends new student records to `students.csv`. Before appending:
1. Check if the file exists
2. If it doesn't exist, create it with headers
3. If it exists, append without writing headers again
4. Handle the case where student_id might already exist (read, check, then append only new ones)

**Success Criteria**:
- Creates file with headers if it doesn't exist
- Appends without duplicate headers
- Prevents duplicate student_ids
- Works correctly on multiple runs

**Hint**: Check if file exists with `os.path.exists()`, read existing IDs before appending

## Quick Reference: Common Writing Patterns

### Pattern 1: Simple Write (csv module)
```python
import csv
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['header1', 'header2'])
    writer.writerow(['value1', 'value2'])
```

### Pattern 2: Dictionary Write
```python
import csv
with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerows(data_list_of_dicts)
```

### Pattern 3: Pandas Simple Write
```python
import pandas as pd
df.to_csv('output.csv', index=False)
```

### Pattern 4: Append Mode
```python
import csv
with open('output.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['new', 'data'])
```

### Pattern 5: Custom Delimiter
```python
import csv
with open('output.tsv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(data)
```

## Common Mistakes and Solutions

### Mistake 1: Forgetting newline=''
```python
# WRONG - causes double spacing on Windows
with open('file.csv', 'w') as f:
    writer = csv.writer(f)

# CORRECT
with open('file.csv', 'w', newline='') as f:
    writer = csv.writer(f)
```

### Mistake 2: Writing Headers When Appending
```python
# WRONG - adds headers every time
with open('file.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()  # Don't do this in append mode!
    writer.writerows(data)

# CORRECT
with open('file.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writerows(data)  # Just write data
```

### Mistake 3: Not Handling Special Characters
```python
# No need to worry - csv module handles it automatically!
data = [['name', 'note'], ['Alice', 'Loves "Python" and coding, too']]
with open('file.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
# Automatically produces: Alice,"Loves ""Python"" and coding, too"
```

## Key Takeaways

1. **Always use `newline=''`** when opening CSV files for writing
2. **DictWriter** is cleaner when working with structured data
3. **Append mode (`'a'`)** adds data; write mode (`'w'`) erases and creates new
4. **The csv module handles escaping** - don't manually quote fields
5. **Pandas is concise** for DataFrame-to-CSV conversion
6. **Control quoting** with `quoting` parameter when needed
7. **Encoding matters** - specify it explicitly for non-ASCII data

## Looking Ahead

You now know how to both read and write CSV files. Next, you'll learn how to modify existing CSV files - combining reading and writing to transform data. You'll update values, add columns, filter rows, and more.

**Next Lesson**: [04 - Modifying CSV Files](04-modifying-csv.md)

---

## Further Exploration

- **CSV dialects**: Creating custom CSV format rules
- **Streaming writes**: Writing data as it's generated
- **Atomic writes**: Using temporary files for safe overwrites
- **Compression**: Writing gzip/bz2 compressed CSV files
