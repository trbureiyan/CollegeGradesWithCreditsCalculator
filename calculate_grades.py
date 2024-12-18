import re
import json

def get_course_data():
    courses = []
    while True:
        course_name = input("Enter course name (or 'done' to finish): ")
        if course_name.lower() == 'done':
            break
        try:
            credits = float(input(f"Enter credits for {course_name}: "))
            grade = float(input(f"Enter grade for {course_name} (type 0 if not available): "))
            if credits < 0 or grade < 0:
                raise ValueError("Credits and grade must be non-negative.")
            courses.append({"name": course_name, "credits": credits, "grade": grade})
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
    return courses

def calculate_final_grade(courses):
    valid_courses = [course for course in courses if course['grade'] > 0]
    total_credits = sum(course['credits'] for course in valid_courses)
    if total_credits == 0:
        return None
    weighted_sum = sum(course['credits'] * course['grade'] for course in valid_courses)
    return weighted_sum / total_credits

def save_grades(all_semesters):
    try:
        with open('grades.json', 'r') as file:
            existing_grades = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        existing_grades = []
    existing_grades.extend(all_semesters)
    with open('grades.json', 'w') as file:
        json.dump(existing_grades, file)

def delete_saved_data():
    confirmation = input("Are you sure you want to delete all saved data? (yes/no): ").lower()
    if confirmation == 'yes':
        with open('grades.json', 'w') as file:
            json.dump([], file)
        print("All saved data has been deleted.")
    else:
        print("Data deletion canceled.")

def main():
    all_semesters = []
    while True:
        print("\nEnter data for a new semester:")
        courses = get_course_data()
        final_grade = calculate_final_grade(courses)
        if final_grade is not None:
            all_semesters.append({"semester": len(all_semesters) + 1, "grade": final_grade})
            print(f"Final grade for this semester: {final_grade:.2f}")
        else:
            print("No valid grades entered for this semester.")
        action = input("Choose an action - (c)ontinue, (d)elete data, (e)xit: ").lower()
        if action == 'c':
            continue
        elif action == 'd':
            delete_saved_data()
            all_semesters = []
        elif action == 'e':
            break
        else:
            print("Invalid option. Exiting.")
            break
    if all_semesters:
        overall_average = sum(s["grade"] for s in all_semesters) / len(all_semesters)
        print(f"\nOverall average grade: {overall_average:.2f}")
        save_grades(all_semesters)
    else:
        print("No grades to save.")

if __name__ == "__main__":
    main()