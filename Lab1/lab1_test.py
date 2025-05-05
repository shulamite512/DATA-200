import Lab_1.lab1_ref as lab1_ref
import unittest
import random
class TestCheckMyGradeApp(unittest.TestCase):
    def setUp(self):
        self.app = lab1_ref.CheckMyGradeApp()

    def test_add_student(self):
        self.app.add_student("test@example.com", "Test", "Student", "DATA101", "A", "90")
        self.assertEqual(len(self.app.students.to_list()), 1)

    def test_add_thousand_student(self):
        for i in range(1000):
            self.app.add_student(f"test{i}@example.com", f"Test{i}", "Student", f"DATA10{i%10}", "A", random.randint(90, 100))
        self.assertEqual(len(self.app.students.to_list()), 1000)

    def test_delete_student(self):
        self.app.add_student("test@example.com", "Test", "Student", "DATA101", "A", "90")
        self.app.delete_student("test@example.com")
        self.assertEqual(len(self.app.students.to_list()), 0)

    def test_modify_student(self):
        self.app.add_student("test@example.com", "Test", "Student", "DATA101", "A", "90")
        self.app.modify_student("test@example.com", first_name="Updated")
        student_list = self.app.students.to_list()
        self.assertEqual(student_list[0].first_name, "Updated")

    def test_search_student(self):
        self.app.add_student("test@example.com", "Test", "Student", "DATA101", "A", "90")
        results = self.app.search_student("test@example.com")
        self.assertEqual(len(results), 1)

    def test_sort_students(self):
        self.app.add_student("test1@example.com", "Test1", "Student", "DATA101", "A", "90")
        self.app.add_student("test2@example.com", "Test2", "Student", "DATA101", "A", "95")
        self.app.sort_students(attribute="marks", reverse=True)
        student_list = self.app.students.to_list()
        self.assertEqual(student_list[0].marks, "95")

    def test_add_course(self):
        self.app.add_course("DATA101", "Intro to Data", "Basic data concepts")
        self.assertEqual(len(self.app.courses), 1)

    def test_delete_course(self):
        self.app.add_course("DATA101", "Intro to Data", "Basic data concepts")
        self.app.delete_course("DATA101")
        self.assertEqual(len(self.app.courses), 0)

    def test_modify_course(self):
        self.app.add_course("DATA101", "Intro to Data", "Basic data concepts")
        self.app.modify_course("DATA101", course_name="Advanced Data")
        self.assertEqual(self.app.courses[0].course_name, "Advanced Data")

    def test_add_professor(self):
        self.app.add_professor("PROF101", "John Doe", "Senior Professor", "DATA101")
        self.assertEqual(len(self.app.professors), 1)

    def test_delete_professor(self):
        self.app.add_professor("PROF101", "John Doe", "Senior Professor", "DATA101")
        self.app.delete_professor("PROF101")
        self.assertEqual(len(self.app.professors), 0)

    def test_modify_professor(self):
        self.app.add_professor("PROF101", "John Doe", "Senior Professor", "DATA101")
        self.app.modify_professor("PROF101", name="Jane Doe")
        self.assertEqual(self.app.professors[0].name, "Jane Doe")

    def test_add_grade(self):
        self.app.add_grade("GRADE1", "A", "90-100")
        self.assertEqual(len(self.app.grades), 1)

    def test_delete_grade(self):
        self.app.add_grade("GRADE1", "A", "90-100")
        self.app.delete_grade("GRADE1")
        self.assertEqual(len(self.app.grades), 0)

    def test_modify_grade(self):
        self.app.add_grade("GRADE1", "A", "90-100")
        self.app.modify_grade("GRADE1", grade="B")
        self.assertEqual(self.app.grades[0].grade, "B")

    def test_add_login_user(self):
        self.app.add_login_user("user@example.com", "password", "student")
        self.assertEqual(len(self.app.login_users), 1)

    def test_delete_login_user(self):
        self.app.add_login_user("user@example.com", "password", "student")
        self.app.delete_login_user("user@example.com")
        self.assertEqual(len(self.app.login_users), 0)

    def test_modify_login_user(self):
        self.app.add_login_user("user@example.com", "password", "student")
        self.app.modify_login_user("user@example.com", role="professor")
        self.assertEqual(self.app.login_users[0].role, "professor")
