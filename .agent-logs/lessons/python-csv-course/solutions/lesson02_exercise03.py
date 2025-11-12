"""
Lesson 02 - Exercise 3: Count and Filter
Solution using csv module to process employee data
"""

import csv

def analyze_employee_data(file_path):
    """
    Analyze employee CSV data to compute various statistics.

    Args:
        file_path: Path to employee CSV file

    Returns:
        Dictionary with analysis results
    """
    # Initialize counters and accumulators
    total_employees = 0
    department_counts = {}
    total_salary = 0
    experienced_employees = []

    # Process file in one pass
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Count total employees
            total_employees += 1

            # Count by department
            department = row['department']
            department_counts[department] = department_counts.get(department, 0) + 1

            # Accumulate salary
            salary = float(row['salary'])
            total_salary += salary

            # Track experienced employees (>5 years)
            years = int(row['years_experience'])
            if years > 5:
                experienced_employees.append({
                    'name': row['name'],
                    'department': department,
                    'years': years
                })

    # Calculate average
    avg_salary = total_salary / total_employees if total_employees > 0 else 0

    # Return results
    return {
        'total_employees': total_employees,
        'department_counts': department_counts,
        'average_salary': avg_salary,
        'experienced_employees': experienced_employees
    }


def print_analysis(results):
    """Pretty print the analysis results"""
    print("="*60)
    print("EMPLOYEE DATA ANALYSIS")
    print("="*60)

    print(f"\nTotal Employees: {results['total_employees']}")

    print("\nEmployees by Department:")
    for dept, count in sorted(results['department_counts'].items()):
        print(f"  {dept}: {count}")

    print(f"\nAverage Salary: ${results['average_salary']:,.2f}")

    print(f"\nExperienced Employees (>5 years): {len(results['experienced_employees'])}")
    for emp in results['experienced_employees']:
        print(f"  - {emp['name']} ({emp['department']}): {emp['years']} years")

    print("="*60)


# Main execution
if __name__ == "__main__":
    # Create sample employee data if it doesn't exist
    sample_data = [
        ['name', 'department', 'salary', 'years_experience'],
        ['Alice Johnson', 'Engineering', '85000', '5'],
        ['Bob Smith', 'Sales', '72000', '3'],
        ['Charlie Brown', 'Engineering', '95000', '8'],
        ['David Lee', 'Marketing', '68000', '4'],
        ['Emma Wilson', 'Engineering', '78000', '2'],
        ['Frank Miller', 'Sales', '81000', '6'],
        ['Grace Davis', 'HR', '65000', '7'],
        ['Henry Martinez', 'Engineering', '92000', '9'],
        ['Ivy Rodriguez', 'Marketing', '71000', '5'],
        ['Jack Anderson', 'Sales', '75000', '4']
    ]

    # Write sample data
    with open('employees_sample.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)

    print("Sample data created: employees_sample.csv\n")

    # Analyze the data
    results = analyze_employee_data('employees_sample.csv')

    # Print results
    print_analysis(results)

    # Bonus: Save experienced employees to new CSV
    with open('experienced_employees.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'department', 'years'])
        writer.writeheader()
        writer.writerows(results['experienced_employees'])

    print("\nExperienced employees saved to: experienced_employees.csv")
