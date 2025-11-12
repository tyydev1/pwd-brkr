# Lesson 02: Reading CSV Files

## Context & Motivation

Reading CSV files is the foundational skill for all CSV operations. Think of it as learning to open a book before you can read it. In real-world applications, you'll constantly need to load data from CSV files - whether it's processing user uploads, analyzing datasets, importing configurations, or building data pipelines.

Python gives you two powerful tools for reading CSV files: the built-in `csv` module and the pandas library. The `csv` module is lightweight and requires no external dependencies - it's perfect when you need simple, straightforward CSV reading. Pandas, on the other hand, is a data analysis powerhouse that treats CSV data as structured DataFrames, enabling complex operations with minimal code.

Understanding both approaches gives you flexibility. For a simple script that processes 1000 rows, the `csv` module is ideal. For data analysis with filtering, aggregation, and transformation, pandas shines. Let's master both.

## Reading CSV with Python's Built-in `csv` Module

### How It Works Under the Hood

The `csv` module reads files line by line, parsing each line into a list of values based on delimiters. It's memory-efficient because it doesn't load the entire file at once - it streams through it. This makes it perfect for large files or when you want fine-grained control.

### Basic CSV Reading

Let's start with the simplest approach - reading a CSV file into a list of lists:

```python
import csv

# Open the file in read mode
with open('students.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Read all rows into a list
    data = list(csv_reader)

    # Print the data
    for row in data:
        print(row)
```

**What's happening here:**
- `open('students.csv', 'r')`: Opens the file in read mode
- `csv.reader(file)`: Creates an iterator that parses CSV format
- `list(csv_reader)`: Converts the iterator to a list of lists
- Each inner list represents one row from the CSV

**Expected output** (for a students.csv file):
```
['name', 'age', 'grade']
['Alice', '15', '10']
['Bob', '16', '11']
['Charlie', '15', '10']
```

Notice that **everything is a string**, including the numbers. The `csv` module doesn't automatically convert data types.

### Reading Row by Row (Memory Efficient)

For large files, don't load everything at once. Process row by row:

```python
import csv

with open('large_dataset.csv', 'r') as file:
    csv_reader = csv.reader(file)

    # Skip the header row
    header = next(csv_reader)
    print(f"Columns: {header}")

    # Process each row one at a time
    for row in csv_reader:
        # Do something with each row
        print(f"Processing: {row[0]}")  # Print first column

        # Your processing logic here
        # This never loads the full file into memory!
```

**Key points:**
- `next(csv_reader)`: Gets the next row (here used to skip header)
- Each iteration reads one row from disk
- Memory usage stays constant regardless of file size
- Perfect for processing millions of rows

### Handling Different Delimiters

Not all CSV files use commas. The `csv` module lets you specify delimiters:

```python
import csv

# Reading a tab-separated file
with open('data.tsv', 'r') as file:
    csv_reader = csv.reader(file, delimiter='\t')
    for row in csv_reader:
        print(row)

# Reading a semicolon-separated file
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    for row in csv_reader:
        print(row)

# Reading a pipe-separated file
with open('data.psv', 'r') as file:
    csv_reader = csv.reader(file, delimiter='|')
    for row in csv_reader:
        print(row)
```

### Using DictReader (Reading as Dictionaries)

When your CSV has headers, `DictReader` makes data access much more intuitive:

```python
import csv

with open('students.csv', 'r') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        # Each row is now a dictionary!
        # Keys are column names from the header
        print(f"Name: {row['name']}, Age: {row['age']}, Grade: {row['grade']}")
```

**Expected output:**
```
Name: Alice, Age: 15, Grade: 10
Name: Bob, Age: 16, Grade: 11
Name: Charlie, Age: 15, Grade: 10
```

**Why this is powerful:**
- Access values by column name instead of index
- More readable code: `row['name']` vs `row[0]`
- Self-documenting: you know what each value represents
- Safer: doesn't break if column order changes

### Handling Different Encodings

Files from different sources may use different character encodings:

```python
import csv

# UTF-8 (most common, default in Python 3)
with open('data_utf8.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)

# Latin-1 (common in older Windows files)
with open('data_latin1.csv', 'r', encoding='latin-1') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)

# Windows-1252 (Windows encoding)
with open('data_windows.csv', 'r', encoding='cp1252') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
```

**Common encoding issues:**
- File has special characters (é, ñ, ü) that look garbled? Try different encoding
- `UnicodeDecodeError`? The encoding doesn't match the file
- When in doubt, try UTF-8 first, then Latin-1

## Reading CSV with Pandas

### Why Pandas?

Pandas treats CSV data as a DataFrame - a powerful table structure that enables:
- Automatic type detection
- Easy column selection and filtering
- Built-in data analysis functions
- Seamless integration with data science tools

### Basic Pandas CSV Reading

```python
import pandas as pd

# Read CSV into a DataFrame
df = pd.read_csv('students.csv')

# Display the data
print(df)
```

**Expected output:**
```
      name  age  grade
0    Alice   15     10
1      Bob   16     11
2  Charlie   15     10
```

Notice the differences from `csv` module:
- Data is in a structured table format
- Numbers are automatically converted to integers
- There's an index column (0, 1, 2)
- Much more readable display

### Exploring the DataFrame

Once loaded, you can inspect your data:

```python
import pandas as pd

df = pd.read_csv('students.csv')

# Display first 5 rows
print(df.head())

# Display last 5 rows
print(df.tail())

# Get basic information
print(df.info())

# Get statistical summary
print(df.describe())

# Get column names
print(df.columns)

# Get shape (rows, columns)
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
```

### Selecting Specific Columns

```python
import pandas as pd

df = pd.read_csv('students.csv')

# Select one column (returns Series)
names = df['name']
print(names)

# Select multiple columns (returns DataFrame)
subset = df[['name', 'grade']]
print(subset)

# Select columns by position
first_two_cols = df.iloc[:, 0:2]  # First two columns
print(first_two_cols)
```

### Advanced Pandas Reading Options

Pandas offers powerful options for reading CSV files:

```python
import pandas as pd

# Skip the first N rows
df = pd.read_csv('data.csv', skiprows=3)

# Only read specific columns
df = pd.read_csv('data.csv', usecols=['name', 'age'])

# Specify data types for columns
df = pd.read_csv('data.csv', dtype={'age': int, 'name': str})

# Handle missing values
df = pd.read_csv('data.csv', na_values=['NA', 'N/A', 'null', ''])

# Use a different delimiter
df = pd.read_csv('data.csv', delimiter=';')

# Use a specific column as the index
df = pd.read_csv('data.csv', index_col='student_id')

# Read only first N rows
df = pd.read_csv('data.csv', nrows=100)

# Parse date columns automatically
df = pd.read_csv('data.csv', parse_dates=['order_date'])

# Handle files without headers
df = pd.read_csv('data.csv', header=None, names=['col1', 'col2', 'col3'])
```

### Reading Large Files with Chunks

When files are too large for memory, read in chunks:

```python
import pandas as pd

# Read in chunks of 1000 rows
chunk_size = 1000
chunks = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    processed_chunk = chunk[chunk['age'] > 18]  # Example: filter
    chunks.append(processed_chunk)

# Combine all chunks
df = pd.concat(chunks, ignore_index=True)
```

**How this works:**
- `chunksize=1000`: Read 1000 rows at a time
- Each iteration gives you a smaller DataFrame
- Process each chunk independently
- Combine results at the end (if needed)

## Comparison: csv Module vs Pandas

| Feature | csv Module | Pandas |
|---------|-----------|--------|
| **Setup** | Built-in | Requires installation |
| **Memory** | Very efficient | Higher overhead |
| **Speed** | Faster for simple reading | Slower initial load, faster operations |
| **Data Types** | Everything is string | Automatic type detection |
| **Ease of Use** | Manual processing | Rich built-in methods |
| **Best For** | Simple parsing, large files | Data analysis, transformation |

### When to Use Each

**Use `csv` module when:**
- Processing very large files line by line
- Need minimal dependencies
- Simple extraction or transformation
- Writing lightweight scripts

**Use `pandas` when:**
- Analyzing data
- Complex filtering and aggregation
- Need automatic type conversion
- Working with multiple datasets

## Interactive Exercises

### Exercise 1 [Beginner]: Read and Display

**Goal**: Learn basic CSV reading and iteration

**Task**: Create a CSV file called `books.csv` with these columns: title, author, year, pages. Add at least 3 books. Write a Python script that reads this file and prints each book's information in a formatted way.

**Success Criteria**:
- Script reads the CSV correctly
- Prints each book on a separate line
- Output is formatted nicely (not just raw lists)

**Hint**: Use `DictReader` for easier access to columns by name

<details>
<summary>Sample books.csv content</summary>

```csv
title,author,year,pages
The Hobbit,J.R.R. Tolkien,1937,310
1984,George Orwell,1949,328
Dune,Frank Herbert,1965,688
```
</details>

### Exercise 2 [Beginner]: Selective Reading

**Goal**: Practice reading specific columns

**Task**: Using the sample-data/products.csv file (or create one with: product_name, category, price, stock), read only the product_name and price columns using pandas. Display them in a clean format.

**Success Criteria**:
- Only specified columns are loaded
- Data displays correctly
- Use pandas for this exercise

**Hint**: Use the `usecols` parameter in `read_csv()`

### Exercise 3 [Intermediate]: Count and Filter

**Goal**: Learn to iterate and filter CSV data

**Task**: Create a CSV file with employee data: name, department, salary, years_experience. Write a script using the `csv` module that:
1. Counts total number of employees
2. Counts employees per department
3. Finds the average salary
4. Lists employees with > 5 years experience

**Success Criteria**:
- All four pieces of information are calculated correctly
- Uses the csv module (not pandas)
- Processes data in one pass through the file

**Hint**: Use a dictionary to track department counts. Remember to convert string numbers to int/float for calculations.

### Exercise 4 [Intermediate]: Pandas Exploration

**Goal**: Master DataFrame inspection methods

**Task**: Download or create a CSV with at least 50 rows of sales data: date, product, quantity, price. Use pandas to:
1. Display the first 10 rows
2. Show summary statistics
3. Find the product that sold the most quantity
4. Calculate total revenue (quantity × price)

**Success Criteria**:
- Uses pandas effectively
- All four operations complete correctly
- Code is concise (leverage pandas built-ins)

**Hint**: Use `groupby()` to aggregate by product, and create a new column for revenue

### Exercise 5 [Advanced]: Chunked Processing

**Goal**: Learn memory-efficient processing for large files

**Task**: Create or find a CSV with at least 10,000 rows. Write a script that processes it in chunks of 1000 rows and:
1. Counts total rows processed
2. Tracks how many chunks were processed
3. Finds the maximum value in a numeric column across all chunks

**Success Criteria**:
- File is never fully loaded into memory
- Correct count of rows and chunks
- Maximum value is correctly identified

**Hint**: Keep a running variable outside the chunk loop to track the overall maximum

## Quick Reference: Common Reading Patterns

### Pattern 1: Quick Read (Small Files)
```python
import pandas as pd
df = pd.read_csv('data.csv')
```

### Pattern 2: Memory-Efficient Read (Large Files)
```python
import csv
with open('data.csv', 'r') as f:
    for row in csv.reader(f):
        process(row)
```

### Pattern 3: Dictionary Access
```python
import csv
with open('data.csv', 'r') as f:
    for row in csv.DictReader(f):
        print(row['column_name'])
```

### Pattern 4: Selective Column Reading
```python
import pandas as pd
df = pd.read_csv('data.csv', usecols=['col1', 'col2'])
```

### Pattern 5: Chunked Reading
```python
import pandas as pd
for chunk in pd.read_csv('data.csv', chunksize=1000):
    process(chunk)
```

## Key Takeaways

1. **Two tools, two purposes**: Use `csv` for simple tasks, pandas for analysis
2. **Memory matters**: For large files, stream row-by-row or use chunks
3. **Encoding is critical**: Always specify encoding when you know it
4. **DictReader is your friend**: Column names beat indices for readability
5. **Pandas automates type conversion**: But you can override with `dtype`
6. **Reading is just the start**: You'll transform what you read in later lessons

## Looking Ahead

Now you can read CSV files into Python programs. In the next lesson, you'll learn the flip side: writing data to CSV files. You'll create CSVs from scratch, learn different writing modes, and handle special characters.

**Next Lesson**: [03 - Writing CSV Files](03-writing-csv.md)

---

## Further Exploration

- **CSV dialects**: Custom parsing rules for unusual CSV formats
- **Error handling**: Using try-except for robust CSV reading
- **Binary mode**: When and why to use `'rb'` instead of `'r'`
- **BOM (Byte Order Mark)**: Handling UTF-8 files with BOM signatures
