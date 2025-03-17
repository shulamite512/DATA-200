import csv
import hashlib
import time
import unittest

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def to_list(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def delete(self, email_address):
        current = self.head
        previous = None

        while current:
            if current.data.email_address == email_address:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return
            previous = current
            current = current.next
        raise ValueError(f"Student with email {email_address} not found.")

    def modify(self, email_address, first_name=None, last_name=None, course_id=None, grades=None, marks=None):
        current = self.head
        while current:
            if current.data.email_address == email_address:
                if first_name:
                    current.data.first_name = first_name
                if last_name:
                    current.data.last_name = last_name
                if course_id:
                    current.data.course_id = course_id
                if grades:
                    current.data.grades = grades
                if marks:
                    current.data.marks = marks
                return
            current = current.next
        raise ValueError(f"Student with email {email_address} not found.")

    def search(self, search_term, attribute="email_address"):
        start_time = time.time()
        results = []
        current = self.head
        while current:
            student = current.data
            if attribute == "email_address" and search_term.lower() in student.email_address.lower():
                results.append(student)
            elif attribute == "first_name" and search_term.lower() in student.first_name.lower():
                results.append(student)
            elif attribute == "last_name" and search_term.lower() in student.last_name.lower():
                results.append(student)
            elif attribute == "course_id" and search_term.lower() in student.course_id.lower():
                results.append(student)

            current = current.next
        end_time = time.time()
        print(f"Search time: {end_time - start_time:.4f} seconds")
        return results

    def sort(self, attribute="first_name", reverse=False):
        start_time = time.time()
        student_list = self.to_list()
        student_list.sort(key=lambda student: getattr(student, attribute), reverse=reverse)

        self.head = None
        for student in student_list:
            self.append(student)

        end_time = time.time()
        print(f"Sort time: {end_time - start_time:.4f} seconds")

class Student:
    def __init__(self, email_address, first_name, last_name, course_id, grades, marks):
        if not email_address or not course_id:
             raise ValueError("Email address and Course ID cannot be empty.")
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grades = grades
        self.marks = marks

    def display_record(self):
        print(f"Name: {self.first_name} {self.last_name}, Email: {self.email_address}, Course ID: {self.course_id}, Grade: {self.grades}, Marks: {self.marks}")

    def update_record(self, first_name=None, last_name=None, course_id=None, grades=None, marks=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if course_id:
            self.course_id = course_id
        if grades:
            self.grades = grades
        if marks:
            self.marks = marks

class Course:
    def __init__(self, course_id, course_name, description):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description

    def display_course(self):
        print(f"Course ID: {self.course_id}, Name: {self.course_name}, Description: {self.description}")

class Professor:
    def __init__(self, professor_id, name, rank, course_id):
        self.professor_id = professor_id
        self.name = name
        self.rank = rank
        self.course_id = course_id

    def display_details(self):
        print(f"Professor ID: {self.professor_id}, Name: {self.name}, Rank: {self.rank}, Course ID: {self.course_id}")

class Grade:
    def __init__(self, grade_id, grade, marks_range):
        self.grade_id = grade_id
        self.grade = grade
        self.marks_range = marks_range

    def display_grade(self):
        print(f"Grade ID: {self.grade_id}, Grade: {self.grade}, Marks Range: {self.marks_range}")

class LoginUser:
    def __init__(self, email_id, password, role):
        self.email_id = email_id
        self.password = self.encrypt_password(password)
        self.role = role

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def decrypt_password(self, encrypted_password, entered_password):
         return hashlib.sha256(entered_password.encode()).hexdigest() == encrypted_password

    def login(self, entered_password):
        encrypted_password = self.password
        if self.decrypt_password(encrypted_password, entered_password):
            print("Login successful!")
            return True
        else:
            print("Login failed.")
            return False

    def change_password(self, new_password):
        self.password = self.encrypt_password(new_password)
        print("Password changed successfully.")

class CheckMyGradeApp:
    def __init__(self):
        self.students = LinkedList()
        self.courses = []
        self.professors = []
        self.login_users = []
        self.grades = []

    def load_data(self, filename, data_type):
         try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        if data_type == "students":
                            student = Student(row['Email_address'], row['First_name'], row['Last_name'], row['Course.id'], row['grades'], row['Marks'])
                            self.students.append(student)
                        elif data_type == "courses":
                            self.courses.append(Course(row['Course_id'], row['Course_name'], row['Description']))
                        elif data_type == "professors":
                            self.professors.append(Professor(row['Professor_id'], row['Professor_Name'], row['Rank'], row['Course.id']))
                        elif data_type == "login":
                            self.login_users.append(LoginUser(row['User_id'], row['Password'], row['Role']))
                        elif data_type == "grades":
                            self.grades.append(Grade(row['Grade_id'], row['Grade'], row['Marks range']))
                    except ValueError as ve:
                        print(f"Skipping row due to data error: {ve}")
                    except KeyError as ke:
                        print(f"Skipping row due to missing column: {ke}")

         except FileNotFoundError:
            print(f"Error: {filename} not found.")
         except Exception as e:
            print(f"Error loading data from {filename}: {e}")

    def save_data(self, filename, data, data_type):
        if data_type == "students":
             header = ['Email_address', 'First_name', 'Last_name', 'Course.id', 'grades', 'Marks']
             data = self.students.to_list()
        elif data_type == "courses":
            header = ['Course_id', 'Course_name', 'Description']
        elif data_type == "professors":
            header = ['Professor_id', 'Professor_Name', 'Rank', 'Course.id']
        elif data_type == "login":
            header = ['User_id', 'Password', 'Role']
        elif data_type == "grades":
            header = ['Grade_id', 'Grade', 'Marks range']
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
                if data_type == "students":
                   for student in data:
                        writer.writerow({'Email_address': student.email_address, 'First_name': student.first_name, 'Last_name': student.last_name, 'Course.id': student.course_id, 'grades': student.grades, 'Marks': student.marks})
                elif data_type == "courses":
                    for course in data:
                         writer.writerow({'Course_id': course.course_id, 'Course_name': course.course_name, 'Description': course.description})
                elif data_type == "professors":
                     for professor in data:
                         writer.writerow({'Professor_id': professor.professor_id, 'Professor_Name': professor.name, 'Rank': professor.rank, 'Course.id': professor.course_id})
                elif data_type == "login":
                    for user in data:
                        writer.writerow({'User_id': user.email_id, 'Password': user.password, 'Role': user.role})
                elif data_type == "grades":
                    for grade in data:
                         writer.writerow({'Grade_id': grade.grade_id, 'Grade': grade.grade, 'Marks range': grade.marks_range})

            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data to {filename}: {e}")


    def add_student(self, email_address, first_name, last_name, course_id, grades, marks):
        try:
            student = Student(email_address, first_name, last_name, course_id, grades, marks)
            self.students.append(student)
            print(f"Student {first_name} {last_name} added.")
        except ValueError as e:
            print(f"Error adding student: {e}")

    def delete_student(self, email_address):
        try:
            self.students.delete(email_address)
            print(f"Student with email {email_address} deleted.")
        except ValueError as e:
            print(f"Error deleting student: {e}")

    def modify_student(self, email_address, first_name=None, last_name=None, course_id=None, grades=None, marks=None):
        try:
            self.students.modify(email_address, first_name, last_name, course_id, grades, marks)
            print(f"Student with email {email_address} modified.")
        except ValueError as e:
            print(f"Error modifying student: {e}")

    def search_student(self, search_term, attribute="email_address"):
        return self.students.search(search_term, attribute)

    def sort_students(self, attribute="first_name", reverse=False):
        self.students.sort(attribute, reverse)


    def average_score(self, course_id):
        scores = []
        current = self.students.head
        while current:
            if current.data.course_id == course_id:
                try:
                    scores.append(float(current.data.marks))
                except ValueError:
                    print(f"Invalid marks for student {current.data.email_address}, skipping.")
            current = current.next
        if scores:
            return sum(scores) / len(scores)
        else:
            return None

    def median_score(self, course_id):
        scores = []
        current = self.students.head
        while current:
            if current.data.course_id == course_id:
                try:
                    scores.append(float(current.data.marks))
                except ValueError:
                    print(f"Invalid marks for student {current.data.email_address}, skipping.")
            current = current.next
        if scores:
            scores.sort()
            mid = len(scores) // 2
            return (scores[mid - 1] + scores[mid]) / 2 if len(scores) % 2 == 0 else scores[mid]
        else:
            return None

    def course_report(self, course_id):
        print(f"Course Report for {course_id}:")
        current = self.students.head
        while current:
            if current.data.course_id == course_id:
                current.data.display_record()
            current = current.next

    #Professor Report
    def professor_report(self, professor_id):
        print(f"Professor Report for {professor_id}:")
        for professor in self.professors:
            if professor.professor_id == professor_id:
                current = self.students.head
                while current:
                    if current.data.course_id == professor.course_id:
                        current.data.display_record()
                    current = current.next
    # Student Report
    def student_report(self, email_address):
        print(f"Student Report for {email_address}:")
        current = self.students.head
        while current:
            if current.data.email_address == email_address:
                current.data.display_record()
                return
            current = current.next
        print(f"Student with email {email_address} not found.")

    def add_course(self, course_id, course_name, description):
        if not course_id:
            print("Course ID cannot be empty.")
            return
        try:
            course = Course(course_id, course_name, description)
            self.courses.append(course)
            print(f"Course {course_name} added.")
        except Exception as e:
            print(f"Error adding course: {e}")

    def delete_course(self, course_id):
        try:
            self.courses = [course for course in self.courses if course.course_id != course_id]
            print(f"Course with ID {course_id} deleted.")
        except Exception as e:
            print(f"Error deleting course: {e}")

    def modify_course(self, course_id, course_name=None, description=None):
        try:
            for course in self.courses:
                if course.course_id == course_id:
                    if course_name:
                        course.course_name = course_name
                    if description:
                        course.description = description
                    print(f"Course with ID {course_id} modified.")
                    return
            print(f"Course with ID {course_id} not found.")
        except Exception as e:
            print(f"Error modifying course: {e}")

    def add_professor(self, professor_id, name, rank, course_id):
        try:
            professor = Professor(professor_id, name, rank, course_id)
            self.professors.append(professor)
            print(f"Professor {name} added.")
        except Exception as e:
            print(f"Error adding professor: {e}")

    def delete_professor(self, professor_id):
        try:
            self.professors = [professor for professor in self.professors if professor.professor_id != professor_id]
            print(f"Professor with ID {professor_id} deleted.")
        except Exception as e:
            print(f"Error deleting professor: {e}")

    def modify_professor(self, professor_id, name=None, rank=None, course_id=None):
        try:
            for professor in self.professors:
                if professor.professor_id == professor_id:
                    if name:
                        professor.name = name
                    if rank:
                        professor.rank = rank
                    if course_id:
                        professor.course_id = course_id
                    print(f"Professor with ID {professor_id} modified.")
                    return
            print(f"Professor with ID {professor_id} not found.")
        except Exception as e:
            print(f"Error modifying professor: {e}")

    def add_grade(self, grade_id, grade, marks_range):
        try:
            grade_obj = Grade(grade_id, grade, marks_range)
            self.grades.append(grade_obj)
            print(f"Grade {grade} added.")
        except Exception as e:
            print(f"Error adding grade: {e}")

    def delete_grade(self, grade_id):
        try:
            self.grades = [grade for grade in self.grades if grade.grade_id != grade_id]
            print(f"Grade with ID {grade_id} deleted.")
        except Exception as e:
            print(f"Error deleting grade: {e}")

    def modify_grade(self, grade_id, grade=None, marks_range=None):
        try:
            for grade_obj in self.grades:
                if grade_obj.grade_id == grade_id:
                    if grade:
                        grade_obj.grade = grade
                    if marks_range:
                        grade_obj.marks_range = marks_range
                    print(f"Grade with ID {grade_id} modified.")
                    return
            print(f"Grade with ID {grade_id} not found.")
        except Exception as e:
            print(f"Error modifying grade: {e}")

    def add_login_user(self, email_id, password, role):
        try:
            login_user = LoginUser(email_id, password, role)
            self.login_users.append(login_user)
            print(f"Login user {email_id} added.")
        except Exception as e:
            print(f"Error adding login user: {e}")

    def delete_login_user(self, email_id):
        try:
            self.login_users = [user for user in self.login_users if user.email_id != email_id]
            print(f"Login user with email {email_id} deleted.")
        except Exception as e:
            print(f"Error deleting login user: {e}")

    def modify_login_user(self, email_id, password=None, role=None):
        try:
            for user in self.login_users:
                if user.email_id == email_id:
                    if password:
                        user.change_password(password)
                    if role:
                        user.role = role
                    print(f"Login user with email {email_id} modified.")
                    return
            print(f"Login user with email {email_id} not found.")
        except Exception as e:
            print(f"Error modifying login user: {e}")

    def run(self):
        while True:
            print("\nCheckMyGrade Application")
            print("1. Load Data from CSV")
            print("2. Save Data to CSV")
            print("3. Add Student")
            print("4. Delete Student")
            print("5. Modify Student")
            print("6. Search Student")
            print("7. Sort Students")
            print("8. Course Report")
            print("9. Professor Report")
            print("10. Student Report")
            print("11. Add Course")
            print("12. Delete Course")
            print("13. Modify Course")
            print("14. Add Professor")
            print("15. Delete Professor")
            print("16. Modify Professor")
            print("17. Add Grade")
            print("18. Delete Grade")
            print("19. Modify Grade")
            print("20. Add Login User")
            print("21. Delete Login User")
            print("22. Modify Login User")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                data_type = input("Enter data type to load (students/courses/professors/login/grades): ")
                filename = input("Enter filename: ")
                self.load_data(filename, data_type)
            elif choice == '2':
                data_type = input("Enter data type to save (students/courses/professors/login/grades): ")
                filename = input("Enter filename: ")
                if data_type == "students":
                    data = self.students
                elif data_type == "courses":
                    data = self.courses
                elif data_type == "professors":
                    data = self.professors
                elif data_type == "login":
                    data = self.login_users
                elif data_type == "grades":
                    data = self.grades
                self.save_data(filename, data, data_type)
            elif choice == '3':
                email = input("Enter student email: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                course_id = input("Enter course ID: ")
                grades = input("Enter grades: ")
                marks = input("Enter marks: ")
                self.add_student(email, first_name, last_name, course_id, grades, marks)
            elif choice == '4':
                email = input("Enter email of student to delete: ")
                self.delete_student(email)
            elif choice == '5':
                email = input("Enter email of student to modify: ")
                first_name = input("Enter new first name (or leave blank): ") or None
                last_name = input("Enter new last name (or leave blank): ") or None
                course_id = input("Enter new course ID (or leave blank): ") or None
                grades = input("Enter new grades (or leave blank): ") or None
                marks = input("Enter new marks (or leave blank): ") or None
                self.modify_student(email, first_name, last_name, course_id, grades, marks)
            elif choice == '6':
                search_term = input("Enter search term: ")
                attribute = input("Enter attribute to search by (email_address/first_name): ") or "email_address"
                results = self.search_student(search_term, attribute)
                for student in results:
                    student.display_record()
            elif choice == '7':
                attribute = input("Enter attribute to sort by (first_name/marks/email_address): ") or "first_name"
                reverse = input("Reverse sort? (yes/no): ").lower() == "yes"
                self.sort_students(attribute, reverse)
                current = self.students.head
                while current:
                    current.data.display_record()
                    current = current.next
            elif choice == '8':
                course_id = input("Enter course ID for report: ")
                self.course_report(course_id)
            elif choice == '9':
                professor_id = input("Enter professor ID for report: ")
                self.professor_report(professor_id)
            elif choice == '10':
                email_address = input("Enter student email for report: ")
                self.student_report(email_address)
            elif choice == '11':
                course_id = input("Enter course ID: ")
                course_name = input("Enter course name: ")
                description = input("Enter course description: ")
                self.add_course(course_id, course_name, description)
            elif choice == '12':
                course_id = input("Enter course ID to delete: ")
                self.delete_course(course_id)
            elif choice == '13':
                course_id = input("Enter course ID to modify: ")
                course_name = input("Enter new course name (or leave blank): ") or None
                description = input("Enter new description (or leave blank): ") or None
                self.modify_course(course_id, course_name, description)
            elif choice == '14':
                professor_id = input("Enter professor ID: ")
                name = input("Enter professor name: ")
                rank = input("Enter professor rank: ")
                course_id = input("Enter course ID: ")
                self.add_professor(professor_id, name, rank, course_id)
            elif choice == '15':
                professor_id = input("Enter professor ID to delete: ")
                self.delete_professor(professor_id)
            elif choice == '16':
                professor_id = input("Enter professor ID to modify: ")
                name = input("Enter new professor name (or leave blank): ") or None
                rank = input("Enter new rank (or leave blank): ") or None
                course_id = input("Enter new course ID (or leave blank): ") or None
                self.modify_professor(professor_id, name, rank, course_id)
            elif choice == '17':
                grade_id = input("Enter grade ID: ")
                grade = input("Enter grade: ")
                marks_range = input("Enter marks range: ")
                self.add_grade(grade_id, grade, marks_range)
            elif choice == '18':
                grade_id = input("Enter grade ID to delete: ")
                self.delete_grade(grade_id)
            elif choice == '19':
                grade_id = input("Enter grade ID to modify: ")
                grade = input("Enter new grade (or leave blank): ") or None
                marks_range = input("Enter new marks range (or leave blank): ") or None
                self.modify_grade(grade_id, grade, marks_range)
            elif choice == '20':
                email_id = input("Enter login user email: ")
                password = input("Enter login user password: ")
                role = input("Enter login user role: ")
                self.add_login_user(email_id, password, role)
            elif choice == '21':
                email_id = input("Enter login user email to delete: ")
                self.delete_login_user(email_id)
            elif choice == '22':
                email_id = input("Enter login user email to modify: ")
                password = input("Enter new password (or leave blank): ") or None
                role = input("Enter new role (or leave blank): ") or None
                self.modify_login_user(email_id, password, role)
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = CheckMyGradeApp()
    app.run()

    # Run unit tests
    # unittest.main()

