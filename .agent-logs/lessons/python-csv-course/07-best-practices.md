# Lesson 07: Error Handling & Best Practices

## Context & Motivation

The difference between a script that works on your laptop and production-ready code is error handling. Real-world CSV files are messy: wrong encodings, missing values, malformed rows, corrupt data, unexpected formats. Your code will encounter these issues, and how you handle them determines whether your program crashes spectacularly or gracefully recovers.

Best practices aren't just about preventing errors - they're about building maintainable, efficient, and professional code. They include choosing appropriate data structures, validating inputs, logging problems, handling edge cases, and optimizing performance. These practices separate hobbyist code from professional software engineering.

This lesson teaches defensive programming for CSV operations. You'll learn to anticipate what can go wrong, handle it elegantly, and build robust data processing pipelines that run reliably in production environments.

## Common CSV Errors and Solutions

### Error 1: File Not Found

The most basic error - file doesn't exist:

```python
import csv
import os
from pathlib import Path

# BAD: No error handling
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    # FileNotFoundError if file doesn't exist!

# GOOD: Check existence first
if os.path.exists('data.csv'):
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        # Process file
else:
    print("Error: data.csv not found")

# BETTER: Use try-except
try:
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            process(row)
except FileNotFoundError:
    print("Error: data.csv not found")
    # Log error, use default data, or exit gracefully

# BEST: Using pathlib (more modern)
from pathlib import Path

file_path = Path('data.csv')
if file_path.exists() and file_path.is_file():
    df = pd.read_csv(file_path)
else:
    print(f"Error: {file_path} not found or is not a file")
```

### Error 2: Encoding Issues

Files created on different systems may use different encodings:

```python
import csv
import pandas as pd

# BAD: Assumes UTF-8 (default)
df = pd.read_csv('data.csv')
# UnicodeDecodeError if file is in different encoding!

# GOOD: Specify encoding explicitly
df = pd.read_csv('data.csv', encoding='utf-8')

# BETTER: Try multiple encodings
def read_csv_flexible(file_path):
    """Try reading CSV with different encodings"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully read with encoding: {encoding}")
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue

    raise ValueError(f"Could not read {file_path} with any standard encoding")

# Usage
try:
    df = read_csv_flexible('data.csv')
except ValueError as e:
    print(e)

# BEST: Detect encoding automatically
import chardet

def detect_encoding(file_path):
    """Detect file encoding"""
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Read first 10KB
        result = chardet.detect(raw_data)
        return result['encoding']

encoding = detect_encoding('data.csv')
print(f"Detected encoding: {encoding}")
df = pd.read_csv('data.csv', encoding=encoding)
```

**Common encodings:**
- `utf-8`: Modern standard, supports all characters
- `latin-1` / `iso-8859-1`: Western European
- `cp1252`: Windows Western European
- `ascii`: Basic English characters only

### Error 3: Malformed CSV (Inconsistent Columns)

Rows have different numbers of columns:

```python
import csv
import pandas as pd

# BAD: No handling
df = pd.read_csv('malformed.csv')
# May work but data is corrupted, or raises ParserError

# GOOD: Handle with csv module
def read_csv_robust(file_path):
    """Read CSV handling inconsistent columns"""
    rows = []
    errors = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        expected_cols = len(header)

        for line_num, row in enumerate(reader, start=2):
            if len(row) == expected_cols:
                rows.append(row)
            elif len(row) < expected_cols:
                # Pad with empty strings
                row.extend([''] * (expected_cols - len(row)))
                rows.append(row)
                errors.append(f"Line {line_num}: Too few columns, padded")
            else:
                # Truncate extra columns
                rows.append(row[:expected_cols])
                errors.append(f"Line {line_num}: Too many columns, truncated")

    if errors:
        print(f"Fixed {len(errors)} malformed rows")
        for error in errors[:5]:  # Show first 5
            print(f"  - {error}")

    return pd.DataFrame(rows, columns=header)

# Usage
df = read_csv_robust('malformed.csv')

# PANDAS: Use error_bad_lines parameter (pandas < 1.3)
# Or on_bad_lines parameter (pandas >= 1.3)
df = pd.read_csv(
    'malformed.csv',
    on_bad_lines='skip',  # Skip bad lines
    # on_bad_lines='warn',  # Skip but warn
)
```

### Error 4: Type Conversion Errors

Data that should be numeric contains non-numeric values:

```python
import pandas as pd
import numpy as np

# BAD: Assume all values are numeric
df = pd.read_csv('data.csv')
df['age'] = df['age'].astype(int)
# ValueError if 'age' contains non-numeric values!

# GOOD: Handle conversion errors
df = pd.read_csv('data.csv')
df['age'] = pd.to_numeric(df['age'], errors='coerce')
# Converts invalid values to NaN

# BETTER: Track what failed
df = pd.read_csv('data.csv')
original_ages = df['age'].copy()
df['age'] = pd.to_numeric(df['age'], errors='coerce')

# Report conversion failures
failed_conversions = df[df['age'].isna() & original_ages.notna()]
if not failed_conversions.empty:
    print(f"Warning: {len(failed_conversions)} invalid age values found:")
    print(failed_conversions[['name', 'age']])

# BEST: Validate before conversion
def safe_to_numeric(series, column_name):
    """Convert to numeric with validation"""
    original = series.copy()
    converted = pd.to_numeric(series, errors='coerce')

    num_failed = converted.isna().sum() - original.isna().sum()

    if num_failed > 0:
        print(f"Warning: {num_failed} values in '{column_name}' could not be converted")
        # Show examples
        failed_indices = converted.isna() & original.notna()
        print("Examples of failed conversions:")
        print(original[failed_indices].head())

    return converted

df['age'] = safe_to_numeric(df['age'], 'age')
```

### Error 5: Missing Required Columns

CSV doesn't have expected columns:

```python
import pandas as pd

# BAD: Assume columns exist
df = pd.read_csv('data.csv')
total = df['price'] * df['quantity']
# KeyError if 'price' or 'quantity' doesn't exist!

# GOOD: Check before accessing
required_columns = ['price', 'quantity', 'product']

df = pd.read_csv('data.csv')
missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Process data
df['total'] = df['price'] * df['quantity']

# BETTER: Comprehensive validation
def validate_dataframe(df, required_cols, optional_cols=None):
    """Validate DataFrame has required columns"""
    missing_required = [col for col in required_cols if col not in df.columns]

    if missing_required:
        raise ValueError(
            f"Missing required columns: {missing_required}\n"
            f"Available columns: {list(df.columns)}"
        )

    if optional_cols:
        missing_optional = [col for col in optional_cols if col not in df.columns]
        if missing_optional:
            print(f"Info: Optional columns not found: {missing_optional}")

    print(f"Validation passed. DataFrame has {len(df)} rows and {len(df.columns)} columns")

# Usage
df = pd.read_csv('data.csv')
validate_dataframe(
    df,
    required_cols=['id', 'name', 'price'],
    optional_cols=['description', 'category']
)
```

## Best Practices for CSV Processing

### Practice 1: Always Close Files Properly

```python
import csv

# BAD: File may not close on error
file = open('data.csv', 'r')
reader = csv.reader(file)
# ... process ...
file.close()

# GOOD: Use context manager (with statement)
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    # ... process ...
# File automatically closes, even if error occurs
```

### Practice 2: Specify Encoding Explicitly

```python
import pandas as pd

# BAD: Relies on system default
df = pd.read_csv('data.csv')

# GOOD: Explicit encoding
df = pd.read_csv('data.csv', encoding='utf-8')

# WRITE: Also specify encoding
df.to_csv('output.csv', encoding='utf-8', index=False)
```

### Practice 3: Validate Input Data

```python
import pandas as pd

def validate_csv_file(file_path, min_rows=1, required_columns=None):
    """Comprehensive CSV validation"""

    # Check file exists
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read CSV
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")

    # Check not empty
    if len(df) < min_rows:
        raise ValueError(f"CSV has {len(df)} rows, minimum {min_rows} required")

    # Check required columns
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    # Check for all-null columns
    null_columns = df.columns[df.isna().all()].tolist()
    if null_columns:
        print(f"Warning: Columns with all null values: {null_columns}")

    # Check for duplicate column names
    if len(df.columns) != len(set(df.columns)):
        duplicates = [col for col in df.columns if list(df.columns).count(col) > 1]
        raise ValueError(f"Duplicate column names: {set(duplicates)}")

    return df

# Usage
try:
    df = validate_csv_file(
        'data.csv',
        min_rows=10,
        required_columns=['id', 'name', 'email']
    )
    print("Validation successful!")
except (FileNotFoundError, ValueError) as e:
    print(f"Validation failed: {e}")
```

### Practice 4: Log Problems Instead of Silently Failing

```python
import csv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csv_processing.log'),
        logging.StreamHandler()
    ]
)

def process_csv_with_logging(file_path):
    """Process CSV with comprehensive logging"""

    logging.info(f"Starting to process {file_path}")

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows_processed = 0
            errors = 0

            for row_num, row in enumerate(reader, start=2):
                try:
                    # Process row
                    if not row.get('email'):
                        logging.warning(f"Row {row_num}: Missing email")
                        errors += 1

                    # More processing...
                    rows_processed += 1

                except Exception as e:
                    logging.error(f"Row {row_num}: {e}")
                    errors += 1

        logging.info(
            f"Processing complete. "
            f"Rows: {rows_processed}, Errors: {errors}"
        )

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

# Usage
process_csv_with_logging('data.csv')
```

### Practice 5: Use Type Hints for Clarity

```python
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path

def read_csv_file(
    file_path: Path,
    required_columns: Optional[List[str]] = None,
    encoding: str = 'utf-8'
) -> pd.DataFrame:
    """
    Read CSV file with validation.

    Args:
        file_path: Path to CSV file
        required_columns: List of column names that must exist
        encoding: File encoding (default: utf-8)

    Returns:
        pandas DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns are missing
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path, encoding=encoding)

    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    return df
```

### Practice 6: Handle Large Files Efficiently

```python
import pandas as pd

def process_large_csv(file_path: str, chunk_size: int = 10000):
    """
    Process large CSV in chunks to manage memory.

    Best practices:
    - Use chunks for files > 100MB
    - Choose chunk_size based on available memory
    - Process and aggregate incrementally
    """

    total_rows = 0
    chunks_processed = 0

    try:
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            # Process chunk
            chunk_filtered = chunk[chunk['value'] > 0]

            # Write to output (append mode)
            chunk_filtered.to_csv(
                'output.csv',
                mode='a',
                header=(chunks_processed == 0),
                index=False
            )

            total_rows += len(chunk)
            chunks_processed += 1

            # Progress logging
            if chunks_processed % 10 == 0:
                print(f"Processed {chunks_processed} chunks ({total_rows:,} rows)")

        print(f"Complete: {chunks_processed} chunks, {total_rows:,} total rows")

    except Exception as e:
        print(f"Error processing chunk {chunks_processed + 1}: {e}")
        raise

# Usage
process_large_csv('huge_file.csv', chunk_size=50000)
```

### Practice 7: Safe File Overwriting

```python
import csv
import os
import shutil
from pathlib import Path

def safe_csv_update(input_file: str, output_file: str, process_func):
    """
    Safely update CSV file using temporary file.

    Pattern:
    1. Write to temporary file
    2. Verify write succeeded
    3. Replace original file atomically
    """

    temp_file = f"{output_file}.tmp"

    try:
        # Process and write to temporary file
        with open(input_file, 'r') as infile, open(temp_file, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                processed_row = process_func(row)
                writer.writerow(processed_row)

        # Verify temp file was created
        if not Path(temp_file).exists():
            raise IOError("Temporary file was not created")

        # Backup original (optional)
        if Path(output_file).exists():
            backup = f"{output_file}.backup"
            shutil.copy2(output_file, backup)

        # Replace original with temp file
        os.replace(temp_file, output_file)

        print(f"Successfully updated {output_file}")

    except Exception as e:
        print(f"Error updating file: {e}")
        # Clean up temp file
        if Path(temp_file).exists():
            os.remove(temp_file)
        raise

# Usage
def price_increase(row):
    row['price'] = str(float(row['price']) * 1.10)
    return row

safe_csv_update('products.csv', 'products_updated.csv', price_increase)
```

## Performance Best Practices

### Tip 1: Choose the Right Tool

```python
import pandas as pd
import csv
import time

# For simple extraction: csv module is faster
def extract_with_csv(file_path):
    result = []
    with open(file_path, 'r') as f:
        for row in csv.DictReader(f):
            if float(row['value']) > 100:
                result.append(row['name'])
    return result

# For complex operations: pandas is better
def extract_with_pandas(file_path):
    df = pd.read_csv(file_path)
    result = df[df['value'] > 100]['name'].tolist()
    return result

# Benchmark
start = time.time()
csv_result = extract_with_csv('data.csv')
csv_time = time.time() - start

start = time.time()
pandas_result = extract_with_pandas('data.csv')
pandas_time = time.time() - start

print(f"CSV module: {csv_time:.4f}s")
print(f"Pandas: {pandas_time:.4f}s")
```

**Guidelines:**
- **csv module**: Simple reading, large files, minimal processing
- **pandas**: Complex transformations, aggregations, analysis

### Tip 2: Use Vectorized Operations

```python
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')

# SLOW: Using apply() with custom function
df['result'] = df['value'].apply(lambda x: x * 2 if x > 0 else 0)

# FAST: Vectorized operation
df['result'] = np.where(df['value'] > 0, df['value'] * 2, 0)

# SLOW: Iterating with iterrows()
for index, row in df.iterrows():
    df.at[index, 'result'] = row['value'] * 2

# FAST: Direct column operation
df['result'] = df['value'] * 2
```

**Speed comparison (1M rows):**
- Vectorized: ~0.1 seconds
- .apply(): ~2-5 seconds
- .iterrows(): ~30+ seconds

### Tip 3: Read Only What You Need

```python
import pandas as pd

# BAD: Read entire file
df = pd.read_csv('huge_file.csv')
df_subset = df[['col1', 'col2']]

# GOOD: Read only needed columns
df = pd.read_csv('huge_file.csv', usecols=['col1', 'col2'])

# BAD: Read all rows then filter
df = pd.read_csv('large_file.csv')
df_filtered = df[df['year'] == 2024]

# BETTER: Read in chunks and filter
chunks = []
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    chunks.append(chunk[chunk['year'] == 2024])
df_filtered = pd.concat(chunks, ignore_index=True)
```

## Interactive Exercises

### Exercise 1 [Intermediate]: Robust File Reader

**Goal**: Build error-resilient CSV reader

**Task**: Write a function that reads a CSV file and handles:
- File not found
- Encoding errors (try multiple encodings)
- Malformed rows (inconsistent columns)
- Empty file

Return a DataFrame and a list of errors encountered.

**Success Criteria**:
- Function doesn't crash on any common error
- Returns valid DataFrame even with some bad rows
- Reports all errors in structured format
- Tries at least 3 encodings

**Hint**: Use try-except blocks for each error type, accumulate errors in a list

### Exercise 2 [Intermediate]: Data Validation

**Goal**: Create comprehensive CSV validator

**Task**: Write a validator that checks:
- Required columns exist
- No duplicate column names
- Specified columns have correct data types
- No completely empty columns
- Minimum row count met

**Success Criteria**:
- Validates all specified requirements
- Returns detailed validation report
- Raises appropriate exceptions with clear messages
- Can handle DataFrames or file paths

**Hint**: Create separate validation functions for each check, combine into main validator

### Exercise 3 [Advanced]: Logging Pipeline

**Goal**: Implement proper logging for CSV processing

**Task**: Create a CSV processing pipeline that:
- Logs start/end times
- Logs progress every N rows
- Logs warnings for data quality issues
- Logs errors but continues processing
- Writes logs to both file and console

**Success Criteria**:
- Uses Python logging module
- Different log levels (INFO, WARNING, ERROR)
- Logs are timestamped
- Both file and console output
- Log file is created automatically

**Hint**: Configure logging at module level with both FileHandler and StreamHandler

### Exercise 4 [Advanced]: Safe File Update

**Goal**: Implement atomic file updates

**Task**: Write a function that updates a CSV file safely:
- Writes to temporary file first
- Creates backup of original
- Only replaces original if writing succeeds
- Cleans up on failure

**Success Criteria**:
- Original file never corrupted
- Backup is created
- Temporary files cleaned up on error
- Uses os.replace() for atomic operation

**Hint**: Use try-except-finally, ensure temp files cleaned in finally block

### Exercise 5 [Expert]: Production-Ready Processor

**Goal**: Build enterprise-grade CSV processor

**Task**: Combine all best practices into one robust processor:
- Validates input file
- Handles encoding detection
- Processes in chunks for memory efficiency
- Logs all operations
- Handles errors gracefully
- Creates safe backups
- Produces processing report

**Success Criteria**:
- Never crashes (catches all exceptions)
- Comprehensive logging
- Memory-efficient for large files
- Detailed success/error report at end
- Well-documented code with type hints
- Could run in production

**Hint**: Break into functions: validate, detect_encoding, process_chunk, main

## Key Takeaways

1. **Always use try-except** for file operations
2. **Specify encoding explicitly** - Don't rely on defaults
3. **Validate inputs** before processing
4. **Log problems** instead of failing silently
5. **Use context managers** (with statement) for file handling
6. **Handle malformed data** gracefully
7. **Choose appropriate tools** - csv vs pandas
8. **Test with bad data** - Don't just test happy path
9. **Use temporary files** for safe updates
10. **Type hints and docstrings** improve maintainability

## Looking Ahead

You've learned professional CSV processing techniques. In the final lesson, you'll apply everything you've learned to build a complete, production-ready CSV data processing application.

**Next Lesson**: [08 - Final Project](08-final-project.md)

---

## Further Exploration

- **Data validation libraries**: Great Expectations, Pandera
- **Schema definition**: Define and validate CSV schemas
- **Testing**: pytest for testing CSV operations
- **Monitoring**: Track CSV processing in production
- **Performance profiling**: cProfile, memory_profiler
