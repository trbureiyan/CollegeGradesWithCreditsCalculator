import re
import json
from tabulate import tabulate

def get_course_data():
    courses = []
    while True:
        course_name = input("\n Enter course name (or 'done' to finish): ")
        if course_name.lower() == 'done':
            break
        try:
            credits = float(input(f"\n Enter credits for {course_name}: "))
            grade = float(input(f"\n Enter grade for {course_name} (type 0 if not available): "))
            if credits < 0 or grade < 0:
                raise ValueError("\n Credits and grade must be non-negative.")
            courses.append({"name": course_name, "credits": credits, "grade": grade})
        except ValueError as e:
            print(f"\n Invalid input: {e}. Please try again.")
    return courses

def calculate_final_grade(courses):
    valid_courses = [course for course in courses if course['grade'] > 0]
    total_credits = sum(course['credits'] for course in valid_courses)
    if total_credits == 0:
        return None
    weighted_sum = sum(course['credits'] * course['grade'] for course in valid_courses)
    return weighted_sum / total_credits

def save_semester(semester_data):
    try:
        with open('grades.json', 'r') as file:
            all_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        all_data = []
    all_data.append(semester_data)
    with open('grades.json', 'w') as file:
        json.dump(all_data, file, indent=4)

def load_all_data():
    try:
        with open('grades.json', 'r') as file:
            all_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        all_data = []
    return all_data

def delete_saved_data():
    confirmation = input("\n Are you sure you want to delete all saved data? (yes/no): ").lower()
    if confirmation == 'yes':
        with open('grades.json', 'w') as file:
            json.dump([], file)
        print("\n All saved data has been deleted.")
    else:
        print("\n Data deletion canceled.")

def display_semester(semester):
    print(f"\n Semester {semester['semester_number']}: Final Grade {semester['final_grade']:.2f}")
    if 'courses' in semester and semester['courses']:
        headers = ['Course Name', 'Credits', 'Grade']
        table = [[course['name'], course['credits'], course['grade']] for course in semester['courses']]
        print(tabulate(table, headers=headers, tablefmt='pretty'))
    else:
        print("\n No courses available for this semester.")

def main_menu():
    while True:
        print("\n--- Grade Calculator Menu ---")
        print("1. Add new semester")
        print("2. View saved semesters")
        print("3. Delete all saved data")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            courses = get_course_data()
            final_grade = calculate_final_grade(courses)
            if final_grade is not None:
                semester_number = len(load_all_data()) + 1
                semester_data = {
                    "semester_number": semester_number,
                    "final_grade": final_grade,
                    "courses": courses
                }
                save_semester(semester_data)
                print(f"\n Semester {semester_number} saved with final grade {final_grade:.2f}.")
            else:
                print("\n No valid grades entered for this semester.")
        elif choice == '2':
            all_data = load_all_data()
            if not all_data:
                print("\n No saved semesters available.")
            else:
                for semester in all_data:
                    display_semester(semester)
        elif choice == '3':
            delete_saved_data()
        elif choice == '4':
            print("\n Exiting the program.")
            break
        else:
            print("\n Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()