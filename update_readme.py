import re
import json
from tabulate import tabulate

def update_readme():
    try:
        with open('grades.json', 'r') as file:
            grades = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        grades = []
    
    semester_sections = []
    if grades:
        overall_average = sum(s["final_grade"] for s in grades) / len(grades)
        for semester in grades:
            semester_number = semester['semester_number']
            final_grade = semester['final_grade']
            courses = semester.get('courses', [])
            if courses:
                headers = ['Course Name', 'Credits', 'Grade']
                table = [[course['name'], course['credits'], course['grade']] for course in courses]
                table_str = tabulate(table, headers=headers, tablefmt='github')
                semester_section = f"### Semester {semester_number}\n\nFinal Grade: **{final_grade:.2f}**\n\n{table_str}\n"
                semester_sections.append(semester_section)
            else:
                semester_sections.append(f"### Semester {semester_number}\n\nNo courses available for this semester.\n")
        grades_content = "\n".join(semester_sections)
        overall_content = f"## Overall Average Grade: **{overall_average:.2f}**\n"
    else:
        grades_content = "No grades available."
        overall_content = ""
    
    with open('README.md', 'r') as file:
        readme_content = file.read()

    new_content = f"""----

## Grade Calculation Application

This application allows you to calculate the final grade for the current semester and the overall average grade for all semesters.

### Usage

1. Enter the course name, credits, and grade for each course.
2. If you don't have a grade for a course, enter `0`.
3. The application will calculate the final grade for the semester and the overall average grade.

{overall_content}

{grades_content}

----
"""

    updated_content = re.sub(r'----.*?----', new_content, readme_content, flags=re.DOTALL)

    with open('README.md', 'w') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()