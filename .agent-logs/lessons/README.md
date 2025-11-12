# Educational Content Library

This directory contains comprehensive educational courses and tutorials created by the concept-teacher agent for learning Python programming and related technologies.

## Directory Structure

```
lessons/
├── README.md                          # This file - guide to the lessons structure
│
├── python-csv-course/                 # Complete Python CSV handling course
│   ├── course-overview.md             # Main course outline and learning path
│   ├── lessons/                       # Individual lesson files
│   │   ├── 01-csv-basics.md
│   │   ├── 02-reading-csv.md
│   │   ├── 03-writing-csv.md
│   │   ├── 04-modifying-csv.md
│   │   ├── 05-advanced-csv.md
│   │   ├── 06-pandas-csv.md
│   │   ├── 07-best-practices.md
│   │   └── 08-final-project.md
│   ├── sample-data/                   # Practice CSV files for exercises
│   ├── solutions/                     # Complete solutions to exercises
│   └── resources/                     # Additional reference materials
│
└── [future-courses]/                  # Additional courses to be added
    ├── course-overview.md
    ├── lessons/
    ├── sample-data/
    └── solutions/
```

## Course: Python CSV File Handling

A comprehensive guide from basic CSV operations to advanced data manipulation techniques.

**Location**: `/home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/`

**Duration**: 8-12 hours total

**Target Audience**: Python programmers with basic language knowledge

### Key Features

- 8 comprehensive lessons covering basics to advanced techniques
- Hands-on exercises with practice data files
- Complete solutions provided for all exercises
- Real-world capstone project
- Coverage of both csv module and pandas library

### Getting Started

1. Begin with the course overview:
   ```
   cat python-csv-course/course-overview.md
   ```

2. Start with Lesson 1:
   ```
   cat python-csv-course/lessons/01-csv-basics.md
   ```

3. Use sample data for practice:
   ```
   ls python-csv-course/sample-data/
   ```

4. Check solutions when needed:
   ```
   ls python-csv-course/solutions/
   ```

## Structure Guidelines

Each course should follow this standard structure:

### Course Directory
```
course-name/
├── course-overview.md          # Overview, learning path, prerequisites
├── lessons/                    # Individual lesson files
│   ├── 01-topic.md
│   ├── 02-topic.md
│   └── ...
├── sample-data/                # CSV/data files for practice
├── solutions/                  # Complete worked solutions
└── resources/                  # Additional references, checklists
```

### Lesson File Format

Each lesson should include:
- Learning objectives
- Concept explanations
- Code examples (with syntax highlighting)
- Hands-on exercises
- Key takeaways
- Links to next lesson and references

### Sample Data Organization

Store practice files in `sample-data/` with clear naming:
- `sample-data/customers.csv`
- `sample-data/sales-data.csv`
- etc.

### Solutions Organization

Store complete solutions in `solutions/` directory:
- `solutions/exercise-01.py`
- `solutions/exercise-02.py`
- etc.

## File Naming Conventions

- **Courses**: Lowercase with hyphens (e.g., `python-csv-course`)
- **Lessons**: Numbered with hyphens (e.g., `01-csv-basics.md`)
- **Data files**: Descriptive names in lowercase with hyphens
- **Solution files**: Match exercise numbers (e.g., `exercise-01.py`)

## Location in Project

The lessons directory is stored in `.agent-logs/lessons/` to keep educational content:
- Separate from main source code
- Out of version control (see .gitignore)
- Organized chronologically through agent logs
- Accessible for AI agent training and reference

## Adding New Courses

When creating new educational content:

1. Create a new directory: `lessons/[course-name]/`
2. Start with a `course-overview.md` file
3. Create a `lessons/` subdirectory for individual lessons
4. Include `sample-data/` and `solutions/` directories
5. Update this README with the new course information

## Managing Educational Content

The `.agent-logs/lessons/` directory is managed by the concept-teacher agent and excluded from git. This allows:
- Free creation and iteration of educational materials
- Automatic organization by date in parent logs folder
- Large educational resources without version control overhead
- Clear separation between source code and educational content

## Quick Navigation

To view a specific course:
```bash
# List all available courses
ls /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/

# Navigate to a course
cd /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/

# View course overview
cat course-overview.md

# List all lessons
ls lessons/
```

## Notes

- All educational content is stored locally and not tracked in git
- The `.agent-logs/` directory is listed in `.gitignore`
- This structure supports scalability for multiple courses
- Lessons are designed for self-paced learning
- Each course is independent and can be studied separately

---

Last updated: 2025-11-12
