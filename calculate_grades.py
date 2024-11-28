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
    return weighted_sum / total_credits if total_credits > 0 else 0

def main():
    all_semesters = []
    while True:
        print("\nEnter data for a new semester:")
        courses = get_course_data()
        final_grade = calculate_final_grade(courses)
        if final_grade is not None:
            all_semesters.append(final_grade)
        print(f"Final grade for this semester: {final_grade:.2f}")
        another_semester = input("Do you want to enter another semester? (yes/no): ").lower()
        if another_semester != 'yes':
            break

    overall_average = sum(all_semesters) / len(all_semesters) if all_semesters else 0
    print(f"\nOverall average grade: {overall_average:.2f}")

if __name__ == "__main__":
    main()