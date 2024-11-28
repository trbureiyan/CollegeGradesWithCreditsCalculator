import re
import json

def update_readme():
    with open('grades.json', 'r') as file:
        grades = json.load(file)

    valid_grades = [grade for grade in grades if isinstance(grade, (int, float))]
    overall_average = sum(valid_grades) / len(valid_grades) if valid_grades else 0

    with open('README.md', 'r') as file:
        readme_content = file.read()

    new_content = [
        "----\n",
        "## Grade Calculation Application\n",
        "This application allows you to calculate the final grade for the current semester and the overall average grade for all semesters.\n",
        "### Usage\n",
        "1. Enter the course name, credits, and grade for each course.\n",
        "2. If you don't have a grade for a course, enter `0`.\n",
        "3. The application will calculate the final grade for the semester and the overall average grade.\n",
        f"Overall average grade: {overall_average:.2f}\n",
        "----\n"
    ]

    updated_content = re.sub(r'----.*?----', ''.join(new_content), readme_content, flags=re.DOTALL)

    with open('README.md', 'w') as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()