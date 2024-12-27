import psycopg2
from pymongo import MongoClient

mongo_config = {
    'host': 'localhost',
    'port': 27017,
    'database': 'university_database_1'
}

def fetch_data(table_name):
    connection = psycopg2.connect(host='localhost', dbname='university_database', user='postgres', password='joy', port=5433)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM public."{table_name}"')
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return records

def connect_mongo():
    client = MongoClient(mongo_config['host'], mongo_config['port'])
    return client[mongo_config['database']]

def transform_students(data):
    students = []
    for student in data:
        student_dict = {
            'student_id': student[0],
            'first_name': student[1],
            'last_name': student[2],
            'gender': student[3],
            'age': student[4],
            'department_id': student[5],
            'courses': [] 
        }
        students.append(student_dict)
    return students

def transform_courses(data):
    """Transform course data into a suitable format for MongoDB."""
    courses = []
    for course in data:
        course_dict = {
            'course_id': course[0],
            'course_name': course[1],
            'credits': course[2],
            'instructor_id': course[3],
            'department_id': course[4],
            'students': []  
        }
        courses.append(course_dict)
    return courses

def transform_enrollments(data):
    enrollments = []
    for enrollment in data:
        enrollments.append({
            'enrollment_id': enrollment[0],
            'student_id': enrollment[1],
            'course_id': enrollment[2],
            'enrollment_date': enrollment[3]
        })
    return enrollments

def transform_instructors(data):
    instructors = []
    for instructor in data:
        instructors.append({
            'instructor_id': instructor[0],
            'first_name': instructor[1],
            'last_name': instructor[2],
            'department_id': instructor[3]
        })
    return instructors

def transform_departments(data):
    departments = []
    for department in data:
        departments.append({
            'department_id': department[0],
            'department_name': department[1]
        })
    return departments

def load_data(mongo_db, students, courses, enrollments, instructors, departments):
    mongo_db.departments.insert_many(departments)
    mongo_db.instructors.insert_many(instructors)

    for course in courses:
        course_enrollments = [
            enrollment for enrollment in enrollments if enrollment['course_id'] == course['course_id']
        ]
        course['students'] = [{
            'student_id': enrollment['student_id'],
            'enrollment_date': enrollment['enrollment_date']
        } for enrollment in course_enrollments]
        mongo_db.courses.insert_one(course)

    for student in students:
        student_enrollments = [
            enrollment for enrollment in enrollments if enrollment['student_id'] == student['student_id']
        ]
        student['courses'] = [{
            'course_id': enrollment['course_id'],
            'enrollment_date': enrollment['enrollment_date']
        } for enrollment in student_enrollments]
        mongo_db.students.insert_one(student)

def main():
    mongo_db = connect_mongo()

    students_data = fetch_data('students')
    courses_data = fetch_data('courses')
    enrollments_data = fetch_data('enrollments')
    instructors_data = fetch_data('instructors')
    departments_data = fetch_data('departments')

    students = transform_students(students_data)
    courses = transform_courses(courses_data)
    enrollments = transform_enrollments(enrollments_data)
    instructors = transform_instructors(instructors_data)
    departments = transform_departments(departments_data)

    load_data(mongo_db, students, courses, enrollments, instructors, departments)

    print("Data migration completed successfully.")

if __name__ == "__main__":
    main()
