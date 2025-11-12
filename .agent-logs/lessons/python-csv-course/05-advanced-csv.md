# Lesson 05: Advanced CSV Techniques

## Context & Motivation

Basic CSV operations work perfectly for small to medium files. But what happens when you encounter a 5GB CSV file with 50 million rows? Loading it entirely into memory crashes your program. What if the CSV uses unusual delimiters or quoting rules? What if you need to process multiple large files simultaneously?

Advanced CSV techniques are about working smarter, not harder. They're the difference between a script that crashes on real-world data and one that handles enterprise-scale datasets effortlessly. You'll learn to process files that dwarf your available RAM, handle edge cases that break naive implementations, and optimize for performance when milliseconds matter.

These techniques aren't just theoretical - they're essential for production systems. Data engineers process terabytes of CSV logs daily. Scientists analyze massive datasets from experiments. Web scrapers handle millions of records. Understanding advanced CSV techniques means your code scales from prototype to production without rewriting.

## Processing Large Files: The Chunking Strategy

### Why Chunking Matters

Consider this: A CSV with 10 million rows, each 100 bytes, is roughly 1GB. Loading it entirely into memory:
- Uses at least 1GB RAM (often 2-3x more due to Python overhead)
- Takes significant time to load
- Leaves little memory for processing
- Crashes if RAM is insufficient

Chunking solves this by processing files in pieces: read 10,000 rows → process → write → read next 10,000 rows. Memory usage stays constant.

### Chunking with csv Module

The `csv` module naturally supports streaming (row-by-row) processing:

```python
import csv

def process_large_file(input_file, output_file):
    """Process large CSV file with constant memory usage"""
    processed_count = 0

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        # Process one row at a time - never loads full file!
        for row in reader:
            # Your processing logic
            row['processed'] = 'yes'

            writer.writerow(row)
            processed_count += 1

            # Optional: Progress indicator
            if processed_count % 100000 == 0:
                print(f"Processed {processed_count:,} rows...")

    print(f"Total rows processed: {processed_count:,}")

# Usage
process_large_file('huge_data.csv', 'huge_data_processed.csv')
```

**Key principle**: The csv reader is an **iterator** - it yields one row at a time from disk. You never hold more than one row in memory.

### Chunking with Pandas

Pandas can process large files in chunks:

```python
import pandas as pd

def process_in_chunks(input_file, output_file, chunk_size=10000):
    """Process large CSV in chunks using pandas"""

    # Initialize: write header to output file
    first_chunk = True

    for chunk in pd.read_csv(input_file, chunksize=chunk_size):
        # Process this chunk
        chunk['new_column'] = chunk['col1'] * chunk['col2']

        # Filter if needed
        chunk = chunk[chunk['col1'] > 0]

        # Write chunk to output
        chunk.to_csv(
            output_file,
            mode='a' if not first_chunk else 'w',  # Append after first chunk
            header=first_chunk,  # Only write header once
            index=False
        )

        first_chunk = False
        print(f"Processed chunk of {len(chunk)} rows")

# Usage
process_in_chunks('large_file.csv', 'processed_file.csv', chunk_size=50000)
```

**How this works:**
1. `chunksize=10000`: Read 10,000 rows at a time
2. Each iteration gives you a smaller DataFrame
3. Process the chunk (filter, transform, etc.)
4. Write to output (append mode after first chunk)
5. Move to next chunk

### Aggregating Results from Chunks

When you need statistics across the entire file:

```python
import pandas as pd

def compute_aggregate_statistics(file_path, chunk_size=10000):
    """Compute stats on large file without loading it all"""

    total_rows = 0
    sum_values = 0
    max_value = float('-inf')
    min_value = float('inf')

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Update statistics from this chunk
        total_rows += len(chunk)
        sum_values += chunk['value'].sum()
        max_value = max(max_value, chunk['value'].max())
        min_value = min(min_value, chunk['value'].min())

    # Calculate final statistics
    mean_value = sum_values / total_rows

    print(f"Total rows: {total_rows:,}")
    print(f"Mean: {mean_value:.2f}")
    print(f"Max: {max_value}")
    print(f"Min: {min_value}")

    return {
        'count': total_rows,
        'mean': mean_value,
        'max': max_value,
        'min': min_value
    }

# Usage
stats = compute_aggregate_statistics('large_data.csv')
```

**Important considerations:**
- Some operations work chunk-by-chunk (sum, max, min, count)
- Others don't (median, percentiles) - they need all data
- For median on huge files, use sampling or specialized tools

## CSV Dialects: Handling Non-Standard Formats

CSV "dialects" define format rules: delimiter, quoting style, line terminator, escape character. The csv module supports custom dialects for unusual formats.

### Understanding Built-in Dialects

Python includes two standard dialects:

```python
import csv

# Excel dialect (default)
# - Comma delimiter
# - Double-quote character
# - Minimal quoting
print(csv.list_dialects())  # ['excel', 'excel-tab', 'unix']

# Inspect a dialect
excel = csv.get_dialect('excel')
print(f"Delimiter: {repr(excel.delimiter)}")  # ','
print(f"Quote char: {repr(excel.quotechar)}")  # '"'
print(f"Line terminator: {repr(excel.lineterminator)}")  # '\r\n'
```

### Creating Custom Dialects

When you encounter non-standard CSV files:

```python
import csv

# Register a custom dialect
csv.register_dialect(
    'pipes',
    delimiter='|',
    quotechar='"',
    quoting=csv.QUOTE_MINIMAL,
    lineterminator='\n',
    skipinitialspace=True  # Ignore spaces after delimiter
)

# Use the custom dialect
with open('pipe_separated.csv', 'r') as file:
    reader = csv.reader(file, dialect='pipes')
    for row in reader:
        print(row)
```

### Inline Dialect Parameters

Instead of registering, specify parameters directly:

```python
import csv

with open('unusual.csv', 'r') as file:
    reader = csv.reader(
        file,
        delimiter=';',
        quotechar="'",
        escapechar='\\',
        doublequote=False,
        skipinitialspace=True
    )
    for row in reader:
        print(row)
```

**Common parameters:**
- `delimiter`: Character separating fields (default: `,`)
- `quotechar`: Character for quoting fields (default: `"`)
- `escapechar`: Character for escaping special chars
- `doublequote`: Whether quotes are escaped by doubling (default: `True`)
- `skipinitialspace`: Ignore whitespace after delimiter
- `lineterminator`: Line ending character (default: `\r\n`)
- `quoting`: When to quote fields (MINIMAL, ALL, NONNUMERIC, NONE)

### Detecting Dialects Automatically

The csv module can guess the dialect:

```python
import csv

with open('unknown_format.csv', 'r') as file:
    # Read a sample of the file
    sample = file.read(1024)

    # Detect the dialect
    dialect = csv.Sniffer().sniff(sample)

    print(f"Detected delimiter: {repr(dialect.delimiter)}")
    print(f"Detected quote char: {repr(dialect.quotechar)}")

    # Reset file pointer to beginning
    file.seek(0)

    # Read using detected dialect
    reader = csv.reader(file, dialect=dialect)
    for row in reader:
        print(row)
```

**Limitations of Sniffer:**
- Requires representative sample
- May fail on unusual formats
- Not 100% reliable - verify results
- Best combined with human validation

## DictReader and DictWriter: Deep Dive

You've seen basic DictReader/DictWriter usage. Let's explore advanced features.

### Handling Missing or Extra Fields

```python
import csv

# DictReader with missing fields in some rows
with open('incomplete.csv', 'r') as file:
    reader = csv.DictReader(file, restkey='extra_fields', restval='MISSING')

    for row in reader:
        print(row)
        # If row has fewer fields than header: missing ones get 'MISSING'
        # If row has more fields than header: extras go in 'extra_fields' list
```

### Custom Field Names (No Header in File)

```python
import csv

# File without header row
fieldnames = ['name', 'age', 'city']

with open('no_header.csv', 'r') as file:
    reader = csv.DictReader(file, fieldnames=fieldnames)

    for row in reader:
        print(f"Name: {row['name']}, Age: {row['age']}")
```

### DictWriter with Extra Fields Control

```python
import csv

data = [
    {'name': 'Alice', 'age': 25, 'extra_field': 'ignored'},
    {'name': 'Bob', 'age': 30}
]

fieldnames = ['name', 'age']

with open('output.csv', 'w', newline='') as file:
    # extrasaction controls what happens with extra fields
    # 'raise': Raise ValueError if row has extra keys
    # 'ignore': Silently ignore extra keys (default)
    writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')

    writer.writeheader()
    writer.writerows(data)
```

## Performance Optimization

### Comparing Approaches: Speed Benchmark

```python
import csv
import pandas as pd
import time

def benchmark_csv_module(file_path):
    """Time csv module reading"""
    start = time.time()

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        row_count = sum(1 for row in reader)

    elapsed = time.time() - start
    return row_count, elapsed

def benchmark_pandas(file_path):
    """Time pandas reading"""
    start = time.time()

    df = pd.read_csv(file_path)
    row_count = len(df)

    elapsed = time.time() - start
    return row_count, elapsed

def benchmark_pandas_chunked(file_path, chunk_size=10000):
    """Time pandas chunked reading"""
    start = time.time()

    row_count = 0
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        row_count += len(chunk)

    elapsed = time.time() - start
    return row_count, elapsed

# Run benchmarks
print("CSV module:", benchmark_csv_module('test_data.csv'))
print("Pandas full:", benchmark_pandas('test_data.csv'))
print("Pandas chunked:", benchmark_pandas_chunked('test_data.csv'))
```

**Typical results for 1M rows:**
- csv module: ~2-3 seconds (most memory efficient)
- pandas full load: ~5-7 seconds (fastest for analysis after loading)
- pandas chunked: ~6-8 seconds (memory efficient, slower than full load)

### When to Use Each Approach

| Scenario | Best Tool | Why |
|----------|-----------|-----|
| File > 1GB | csv module row-by-row | Constant memory |
| Complex transformations | pandas | Rich operations |
| Simple extraction | csv module | Lightweight, fast |
| Aggregations (sum, avg) | pandas chunked | Balance speed and memory |
| Multiple operations | pandas | Operations are vectorized |
| Streaming pipeline | csv module | Natural streaming |

### Memory Profiling

Monitor memory usage of your CSV operations:

```python
import csv
import tracemalloc

def profile_memory(func, *args):
    """Profile memory usage of a function"""
    tracemalloc.start()

    # Run the function
    result = func(*args)

    # Get memory statistics
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

    return result

def load_with_csv(file_path):
    rows = []
    with open(file_path, 'r') as file:
        rows = list(csv.reader(file))
    return len(rows)

def load_with_pandas(file_path):
    import pandas as pd
    df = pd.read_csv(file_path)
    return len(df)

# Profile both approaches
print("CSV module:")
profile_memory(load_with_csv, 'test_data.csv')

print("\nPandas:")
profile_memory(load_with_pandas, 'test_data.csv')
```

## Advanced Filtering and Processing

### Processing with Generator Functions

Generators enable memory-efficient pipelines:

```python
import csv

def read_csv_rows(file_path):
    """Generator: yields rows one at a time"""
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

def filter_rows(rows, condition):
    """Generator: filters rows based on condition"""
    for row in rows:
        if condition(row):
            yield row

def transform_rows(rows, transform_func):
    """Generator: transforms each row"""
    for row in rows:
        yield transform_func(row)

# Build a processing pipeline
rows = read_csv_rows('data.csv')
filtered = filter_rows(rows, lambda r: int(r['age']) > 18)
transformed = transform_rows(filtered, lambda r: {**r, 'adult': 'yes'})

# Write results
with open('output.csv', 'w', newline='') as file:
    writer = None

    for row in transformed:
        if writer is None:
            writer = csv.DictWriter(file, fieldnames=row.keys())
            writer.writeheader()

        writer.writerow(row)
```

**Why this is powerful:**
- Each stage processes one row at a time
- Memory usage stays constant
- Composable: mix and match transformations
- Lazy evaluation: work happens only when needed

### Parallel Processing for Multiple Files

Process multiple CSV files simultaneously:

```python
import csv
import multiprocessing as mp
from pathlib import Path

def process_single_file(file_path):
    """Process one CSV file"""
    count = 0
    total = 0

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            count += 1
            total += float(row['value'])

    return file_path.name, count, total

def process_multiple_files(directory, num_workers=4):
    """Process all CSV files in directory using parallel workers"""

    # Find all CSV files
    csv_files = list(Path(directory).glob('*.csv'))

    # Create worker pool
    with mp.Pool(num_workers) as pool:
        results = pool.map(process_single_file, csv_files)

    # Aggregate results
    for filename, count, total in results:
        print(f"{filename}: {count} rows, total value: {total:.2f}")

# Usage
process_multiple_files('csv_directory/', num_workers=8)
```

**Performance gain:** Near-linear speedup based on CPU cores (4 cores ≈ 4x faster).

## Interactive Exercises

### Exercise 1 [Intermediate]: Chunk-Based Statistics

**Goal**: Learn to compute statistics on large files using chunks

**Task**: Create or download a large CSV file (at least 100K rows) with numeric data. Write a script that computes:
1. Total row count
2. Sum of a numeric column
3. Average of that column
4. Maximum value

Process the file in chunks of 10,000 rows using pandas.

**Success Criteria**:
- File is never fully loaded into memory
- All statistics are computed correctly
- Script prints progress during processing
- Uses pandas chunksize parameter

**Hint**: Keep running totals outside the chunk loop. Average = sum / count.

### Exercise 2 [Intermediate]: Custom Dialect

**Goal**: Handle unusual CSV formats

**Task**: Create a CSV file that uses:
- Semicolons (;) as delimiters
- Single quotes (') as quote characters
- Pipes (|) as escape characters

Write a script that reads this file using a custom dialect and converts it to standard CSV format (commas, double quotes).

**Success Criteria**:
- Correctly reads the unusual format
- Handles quoted fields with delimiters inside
- Outputs standard CSV format
- Uses csv module dialect features

**Hint**: Use `csv.register_dialect()` or pass parameters directly to reader/writer

### Exercise 3 [Advanced]: Memory-Efficient Merge

**Goal**: Merge two large CSV files without loading fully into memory

**Task**: You have two CSV files:
- `orders.csv`: order_id, customer_id, total
- `customers.csv`: customer_id, name, email

Both files are too large for memory. Write a script that:
1. Creates an index (dict) of customer_id → customer data from customers.csv
2. Streams through orders.csv
3. Looks up customer info for each order
4. Writes merged data to `orders_with_customers.csv`

**Success Criteria**:
- customers.csv is read once to build index
- orders.csv is streamed (not loaded fully)
- Output contains merged data
- Memory usage stays reasonable

**Hint**: Read customers.csv into a dict first (assuming it fits), then stream orders.csv

### Exercise 4 [Advanced]: Generator Pipeline

**Goal**: Build composable processing pipeline with generators

**Task**: Create a pipeline that:
1. Reads a CSV file (generator)
2. Filters rows where age > 21 (generator)
3. Transforms: adds `decade` field (age // 10 * 10) (generator)
4. Groups by decade and counts (need to collect results)
5. Writes summary to new CSV

**Success Criteria**:
- Uses generator functions for steps 1-3
- Pipeline is memory-efficient
- Final aggregation works correctly
- Output CSV has: decade, count

**Hint**: Use generator functions with `yield`. For grouping, you'll need to collect results in a dict.

### Exercise 5 [Expert]: Parallel File Processing

**Goal**: Process multiple CSV files in parallel

**Task**: Create 10 CSV files with sales data. Write a script that:
1. Finds all CSV files in a directory
2. Processes each file in parallel (4 workers)
3. Computes total sales per file
4. Aggregates results across all files
5. Writes summary report

**Success Criteria**:
- Uses multiprocessing.Pool
- Correctly aggregates results from all files
- Runs significantly faster than sequential processing
- Handles errors gracefully

**Hint**: Use `multiprocessing.Pool.map()` with a processing function

## Quick Reference: Advanced Patterns

### Pattern 1: Chunked Processing
```python
import pandas as pd
for chunk in pd.read_csv('file.csv', chunksize=10000):
    process(chunk)
```

### Pattern 2: Row-by-Row Streaming
```python
import csv
with open('file.csv', 'r') as f:
    for row in csv.DictReader(f):
        process(row)
```

### Pattern 3: Custom Dialect
```python
import csv
csv.register_dialect('custom', delimiter=';', quotechar="'")
with open('file.csv', 'r') as f:
    reader = csv.reader(f, dialect='custom')
```

### Pattern 4: Generator Pipeline
```python
def read_rows(file):
    for row in csv.DictReader(open(file)):
        yield row

def filter_rows(rows, condition):
    for row in rows:
        if condition(row):
            yield row

pipeline = filter_rows(read_rows('file.csv'), lambda r: r['age'] > 18)
```

### Pattern 5: Parallel Processing
```python
import multiprocessing as mp
with mp.Pool(4) as pool:
    results = pool.map(process_file, file_list)
```

## Key Takeaways

1. **Chunking enables large file processing** - Memory stays constant
2. **csv module is naturally streaming** - Use it for huge files
3. **Dialects handle format variations** - Don't manually parse unusual formats
4. **Generators enable pipelines** - Compose operations efficiently
5. **Parallel processing multiplies throughput** - Use multiple cores
6. **Profile before optimizing** - Measure memory and time
7. **Choose the right tool** - csv for streaming, pandas for analysis

## Looking Ahead

You've mastered advanced CSV techniques for handling edge cases and large-scale data. Next, you'll dive deep into pandas, learning powerful DataFrame operations, complex transformations, and merging multiple datasets.

**Next Lesson**: [06 - Pandas Deep Dive](06-pandas-csv.md)

---

## Further Exploration

- **Dask**: Pandas-like library for larger-than-memory datasets
- **Vaex**: Billion-row DataFrames with lazy evaluation
- **Apache Arrow**: High-performance columnar data format
- **Streaming parsers**: ijson for JSON, ElementTree for XML
