import random
from faker import Faker

# Initialize Faker instance
fake = Faker()

# Define ranges for IDs
NUM_DEPARTMENTS = 10   # Up to 50 departments
NUM_INSTRUCTORS = 200  # Up to 100 instructors
NUM_STUDENTS = 500    # Up to 300 students
NUM_COURSES = 150      # Up to 200 courses
NUM_ENROLLMENTS = 500  # Up to 300 enrollments

# Write SQL insert statements into text files
def write_to_file(filename, data):
    with open(filename, 'w') as file:
        for line in data:
            file.write(line + '\n')

# Generate Departments data
def generate_departments():
    departments = []
    for i in range(1, NUM_DEPARTMENTS + 1):
        department_name = fake.company()[:100]
        building = fake.building_number()[:50]
        budget = round(random.uniform(50000, 500000), 2)
        sql = f"INSERT INTO Departments (department_id, department_name, building, budget) VALUES ({i}, '{department_name}', '{building}', {budget});"
        departments.append(sql)
    return departments

# Generate Instructors data
def generate_instructors():
    instructors = []
    for i in range(1, NUM_INSTRUCTORS + 1):
        first_name = fake.first_name()[:50]
        last_name = fake.last_name()[:50]
        department_id = random.randint(1, NUM_DEPARTMENTS)
        email = fake.email()[:100]
        hire_date = fake.date()
        sql = f"INSERT INTO Instructors (instructor_id, first_name, last_name, department_id, email, hire_date) VALUES ({i}, '{first_name}', '{last_name}', {department_id}, '{email}', '{hire_date}');"
        instructors.append(sql)
    return instructors

# Generate Students data
def generate_students():
    students = []
    for i in range(1, NUM_STUDENTS + 1):
        first_name = fake.first_name()[:50]
        last_name = fake.last_name()[:50]
        gender = random.choice(['M', 'F'])
        age = random.randint(18, 25)
        department_id = random.randint(1, NUM_DEPARTMENTS)
        email = fake.email()[:100]
        enrollment_date = fake.date()
        sql = f"INSERT INTO Students (student_id, first_name, last_name, gender, age, department_id, email, enrollment_date) VALUES ({i}, '{first_name}', '{last_name}', '{gender}', {age}, {department_id}, '{email}', '{enrollment_date}');"
        students.append(sql)
    return students

# Generate Courses data (now includes instructor_id)
def generate_courses():
    courses = []
    for i in range(1, NUM_COURSES + 1):
        course_name = fake.sentence(nb_words=3)[:100]
        course_code = fake.bothify(text='???###')[:10]
        credits = random.randint(1, 5)
        department_id = random.randint(1, NUM_DEPARTMENTS)
        instructor_id = random.randint(1, NUM_INSTRUCTORS)
        sql = f"INSERT INTO Courses (course_id, course_name, course_code, credits, department_id, instructor_id) VALUES ({i}, '{course_name}', '{course_code}', {credits}, {department_id}, {instructor_id});"
        courses.append(sql)
    return courses

# Generate Enrollments data
def generate_enrollments():
    enrollments = []
    for i in range(1, NUM_ENROLLMENTS + 1):
        student_id = random.randint(1, NUM_STUDENTS)
        course_id = random.randint(1, NUM_COURSES)
        grade = random.choice(['A', 'B', 'C', 'D', 'F', 'P', 'NP'])
        enrollment_date = fake.date()
        sql = f"INSERT INTO Enrollments (enrollment_id, student_id, course_id, grade, enrollment_date) VALUES ({i}, {student_id}, {course_id}, '{grade}', '{enrollment_date}');"
        enrollments.append(sql)
    return enrollments

def main():
    # Generate fake data
    departments_data = generate_departments()
    instructors_data = generate_instructors()
    students_data = generate_students()
    courses_data = generate_courses()
    enrollments_data = generate_enrollments()

    # Write to files
    write_to_file('departments_insert.sql', departments_data)
    write_to_file('instructors_insert.sql', instructors_data)
    write_to_file('students_insert.sql', students_data)
    write_to_file('courses_insert.sql', courses_data)
    write_to_file('enrollments_insert.sql', enrollments_data)

    print("Data generation completed successfully.")

if __name__ == "__main__":
    main()
