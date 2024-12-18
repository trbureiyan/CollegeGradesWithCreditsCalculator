import re
import json

def update_readme():
    try:
        with open('grades.json', 'r') as file:
            grades = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        grades = []
    
    if grades:
        overall_average = sum(s["grade"] for s in grades) / len(grades)
        grade_details = "\n".join(
            [f"- Semester {s['semester']}: {s['grade']:.2f}" for s in grades]
        )
    else:
        overall_average = 0
        grade_details = "No grades available."

    with open('README.md', 'r') as file:
        readme_content = file.read()

    new_content = f"""----
## Grade Calculation Application

This application allows you to calculate the final grade for the current semester and the overall average grade for all semesters.

### Usage

1. Enter the course name, credits, and grade for each course.
2. If you don't have a grade for a course, enter `0`.
3. The application will calculate the final grade for the semester and the overall average grade.

### Grades

{grade_details}

**Overall average grade:** {overall_average:.2f}

----
"""

    updated_content = re.sub(r'----.*?----', new_content, readme_content, flags=re.DOTALL)

    with open('README.md', 'w') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()