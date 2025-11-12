# Lesson 01: CSV Basics

## Context & Motivation

CSV (Comma-Separated Values) files are one of the most universal data exchange formats in computing. Despite being simple text files, they power data pipelines in organizations worldwide, from small startups to tech giants. Understanding CSV files is fundamental because they represent the intersection of human readability and machine parsability.

Why do CSV files matter so much? They solve a critical problem: **data portability**. Every spreadsheet application, database system, and programming language can work with CSV files. When you export data from Excel, download transaction history from your bank, or share research data with colleagues, there's a high chance it comes as a CSV file. They're the "lingua franca" of data exchange.

In your journey as a programmer, you'll encounter CSV files constantly. Whether you're building a data analysis tool, importing configuration data, processing logs, or creating reports, CSV files will be your reliable companion. They're lightweight, version-control friendly, and don't require proprietary software to read or write.

## What Is a CSV File?

At its core, a CSV file is a plain text file where each line represents a row of data, and values within each row are separated by commas. Think of it as a spreadsheet saved as text.

### Basic Structure

Here's what a simple CSV file looks like:

```csv
name,age,city
Alice,25,New York
Bob,30,San Francisco
Charlie,35,Seattle
```

This represents a table with three columns (name, age, city) and three rows of data. The first line is typically the **header row** - it defines the column names.

### The Anatomy of CSV

Let's break down the structure:

1. **Header Row** (optional but recommended): The first line containing column names
2. **Data Rows**: Subsequent lines containing actual data values
3. **Delimiter**: The character separating values (usually a comma, hence "Comma-Separated")
4. **Line Breaks**: Separate individual records (rows)

### Visual Representation

```
Column 1    Column 2    Column 3
   ↓           ↓           ↓
name    ,   age    ,   city          ← Header Row
Alice   ,   25     ,   New York      ← Data Row 1
Bob     ,   30     ,   San Francisco ← Data Row 2
Charlie ,   35     ,   Seattle       ← Data Row 3
```

## CSV Variations and Dialects

Not all CSV files look the same. There are several variations:

### Different Delimiters

While commas are standard, other delimiters are used:

```csv
# Tab-separated (TSV)
name    age    city
Alice   25     New York

# Semicolon-separated (common in European locales)
name;age;city
Alice;25;New York

# Pipe-separated
name|age|city
Alice|25|New York
```

**Why different delimiters?** In some countries, commas are used as decimal separators (e.g., "3,14" for pi), so semicolons are used instead. Tab-separated files avoid conflicts when data contains commas.

### Quoted Values

When data contains the delimiter character, quotes protect the value:

```csv
name,description,price
"Widget A","Small, red widget",10.99
"Widget B","Large, blue widget",25.50
```

The commas inside "Small, red widget" don't split the field because it's quoted.

### Escaped Characters

Special characters need escaping:

```csv
name,quote
Alice,"She said, ""Hello World"""
Bob,"He replied, ""Hi there!"""
```

Double quotes inside a quoted field are escaped by doubling them (`""`).

## When to Use CSV Files

### Ideal Use Cases

✅ **Data Exchange Between Systems**
- Exporting from databases
- Importing into spreadsheets
- Sharing datasets between teams

✅ **Simple Tabular Data**
- Flat data structures (no nested objects)
- Consistent column structure
- Text and number data types

✅ **Human-Readable Data**
- Easy to inspect with text editors
- Version control friendly
- Simple debugging

✅ **Lightweight Data Storage**
- No special software required
- Small file size for moderate datasets
- Fast to read and write

### When NOT to Use CSV Files

❌ **Complex Data Structures**
- Nested or hierarchical data → Use JSON or XML
- Multiple related tables → Use a database
- Binary data → Use appropriate binary formats

❌ **Large Datasets**
- Millions of rows → Consider Parquet, HDF5, or databases
- Need for random access → Use indexed formats

❌ **Strict Type Requirements**
- Everything in CSV is text by default
- No native date/time format
- No boolean type (use JSON if types matter)

❌ **Data with Frequent Updates**
- CSVs require full rewrite for modifications
- No concurrent access support
- No transaction safety

## CSV vs Other Formats

### CSV vs JSON

```csv
# CSV - Flat structure
name,age,city
Alice,25,New York
```

```json
// JSON - Can be hierarchical
[
  {
    "name": "Alice",
    "age": 25,
    "address": {
      "city": "New York",
      "state": "NY"
    }
  }
]
```

**Use CSV when**: Data is flat, file size matters, spreadsheet compatibility needed
**Use JSON when**: Data is nested, need to preserve types, working with APIs

### CSV vs Excel (.xlsx)

| Feature | CSV | Excel |
|---------|-----|-------|
| File size | Small | Larger |
| Formulas | No | Yes |
| Formatting | No | Yes |
| Multiple sheets | No | Yes |
| Data types | Text only | Multiple types |
| Universal compatibility | Excellent | Good |

**Use CSV when**: Sharing raw data, automation, version control
**Use Excel when**: Need formulas, formatting, or multiple sheets

### CSV vs Database

**Use CSV when**:
- Small to medium datasets (< 1 million rows)
- One-time data transfer
- Simple read/write operations

**Use Database when**:
- Large datasets needing indexing
- Complex queries with JOIN operations
- Multiple concurrent users
- Data integrity constraints needed

## Real-World CSV Examples

### Example 1: E-commerce Orders

```csv
order_id,customer_name,product,quantity,price,order_date
1001,John Smith,Laptop,1,899.99,2024-01-15
1002,Jane Doe,Mouse,2,25.50,2024-01-15
1003,Bob Johnson,Keyboard,1,75.00,2024-01-16
```

### Example 2: Sensor Data

```csv
timestamp,sensor_id,temperature,humidity
2024-01-15 10:00:00,S001,22.5,45.2
2024-01-15 10:05:00,S001,22.7,45.1
2024-01-15 10:10:00,S001,23.0,44.9
```

### Example 3: Student Grades

```csv
student_id,name,math,science,english
1001,Alice Johnson,95,88,92
1002,Bob Smith,78,85,90
1003,Charlie Brown,92,95,88
```

## Common CSV Challenges

### Challenge 1: Inconsistent Encoding
CSV files can be in different encodings (UTF-8, Latin-1, etc.). Opening a UTF-8 file as Latin-1 causes garbled text.

### Challenge 2: Missing Values
How do you represent "no data"? Empty fields, NULL, N/A, or -1?

```csv
name,age,city
Alice,25,New York
Bob,,San Francisco  # Missing age
Charlie,35,         # Missing city
```

### Challenge 3: Data Type Ambiguity
Everything is text in CSV. Is "01" the number 1 or the string "01"? Is "2024-01-15" a date or just text?

### Challenge 4: Special Characters
Commas in data, newlines in text fields, quotes - all need special handling.

```csv
name,bio
Alice,"Loves coding,
reading, and hiking"  # Multi-line field
```

## Key Takeaways

1. **CSV files are plain text** - You can open them in any text editor
2. **They're universally compatible** - Every platform can read them
3. **They're simple but limited** - Great for flat data, not complex structures
4. **Standardization varies** - Different systems may interpret CSV slightly differently
5. **They're the go-to for data exchange** - When in doubt, export as CSV

## Quick Reference: CSV Terminology

| Term | Definition |
|------|------------|
| **Delimiter** | Character separating values (usually comma) |
| **Header Row** | First row containing column names |
| **Field** | A single data value (cell) |
| **Record** | A complete row of data |
| **Quoting** | Wrapping fields in quotes to handle special characters |
| **Escape Character** | Character used to include special characters literally |
| **Dialect** | Specific set of CSV format rules |

## Looking Ahead

Now that you understand what CSV files are and when to use them, you're ready to learn how to work with them in Python. In the next lesson, we'll dive into reading CSV files using Python's built-in tools and the powerful pandas library.

You'll learn:
- How to open and read CSV files
- Different reading methods and their trade-offs
- Handling various CSV formats and delimiters
- Working with headers and data types

**Next Lesson**: [02 - Reading CSV Files](02-reading-csv.md)

---

## Further Exploration

- **RFC 4180**: The official CSV specification (though rarely followed strictly)
- **CSV vs TSV**: When tabs are better than commas
- **CSV in databases**: How databases import/export CSV
- **Streaming CSV**: Processing files too large for memory
