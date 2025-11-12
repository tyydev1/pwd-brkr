# Quick Reference - Educational Content Organization

## Accessing the Lessons

### View All Available Content
```bash
ls /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/
```

### Start a Course
```bash
cd /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/
cat README.md
```

### Read a Lesson
```bash
cat /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/lessons/01-csv-basics.md
```

### Access Course Overview
```bash
cat /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/course-overview.md
```

### Find Sample Data
```bash
ls /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/sample-data/
```

### Check Solutions
```bash
ls /home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/solutions/
```

## Directory Structure Quick View

```
.agent-logs/
├── ORGANIZATION_SUMMARY.md          # This implementation report
├── QUICK_REFERENCE.md                # This file
└── lessons/
    ├── README.md                     # Master guide
    ├── STRUCTURE.md                  # Detailed structure docs
    └── python-csv-course/
        ├── README.md                 # Course quick start
        ├── course-overview.md        # Full course outline
        ├── lessons/
        │   ├── 01-csv-basics.md
        │   ├── 02-reading-csv.md     # Coming soon
        │   └── ...                   # More lessons
        ├── sample-data/              # Practice CSV files
        ├── solutions/                # Exercise solutions
        └── resources/                # Reference guides
```

## Key Files to Read

### First Time?
1. Read: `/home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/README.md`
2. Then: `/home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/README.md`

### Want Course Details?
- `/home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/course-overview.md`

### Understanding the Organization?
- `/home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/STRUCTURE.md`

### Need Implementation Summary?
- `/home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/ORGANIZATION_SUMMARY.md`

## Common Tasks

### Adding a New Lesson
1. Create file: `lessons/python-csv-course/lessons/NN-topic.md`
2. Follow lesson format: objectives, concepts, examples, exercises
3. Add solutions to: `lessons/python-csv-course/solutions/`

### Adding a New Course
1. Create directory: `lessons/[course-name]/`
2. Create subdirectories: `lessons/sample-data/solutions/resources/`
3. Add `README.md` and `course-overview.md`
4. Add lessons to `lessons/` subdirectory

### Viewing Course Progress
- Total lessons: See `course-overview.md`
- Completed: Check `lessons/` directory
- Available samples: Check `sample-data/`
- Available solutions: Check `solutions/`

## Important Notes

- Educational content is stored in `.agent-logs/` (excluded from git)
- Lessons are independent files, can be read in any order
- Each course is self-contained in its own directory
- Sample data is provided for all exercises
- Complete solutions are available after attempting exercises

## Python CSV Course Overview

- 8 comprehensive lessons
- 8-12 hours total learning time
- Covers csv module and pandas
- Real-world capstone project
- Best practices for production code

**Start here**: `/home/razkar/Workspace/GitHub/tyydev1/pwd-brkr/.agent-logs/lessons/python-csv-course/lessons/01-csv-basics.md`

---
Last updated: 2025-11-12
