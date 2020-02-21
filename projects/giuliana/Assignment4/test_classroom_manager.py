from unittest import TestCase
import classroom_manager as cm

class TestStudent(TestCase):

    def setUp(self):
        self.student = cm.Student(123, 'Anthony', 'Giuliano')
        self.assignment = cm.Assignment('Test Assignment', 100)
    
    def testStudentInit(self):
        self.assertEqual(self.student.id, 123)
        self.assertEqual(self.student.first_name, 'Anthony')
        self.assertEqual(self.student.last_name, 'Giuliano')
        self.assertEqual(self.student.assignments, [])

    def testStudentGetFullName(self):
        self.assertEqual(self.student.get_full_name(), 'Anthony Giuliano')

    def testSubmitAssignment(self):
        count = len(self.student.assignments)
        self.student.submit_assignment(self.assignment)
        count += 1
        self.assertEqual(self.student.assignments[-1], self.assignment)
        self.assertEqual(len(self.student.assignments), count)

    def testGetAssignments(self):
        self.student.submit_assignment(self.assignment)
        self.student.submit_assignment(cm.Assignment('name', 100))
        self.assertEqual(self.student.assignments, self.student.get_assignments())

    def testGetAssignment(self):
        self.student.submit_assignment(self.assignment)
        self.assertEqual(self.assignment, self.student.get_assignment(self.assignment.name))
        self.assertIsNone(self.student.get_assignment('does not exist'))

    def testGetAverage(self):
        self.student.submit_assignment(self.assignment)
        assignment2 = cm.Assignment('assignment2', 80)
        assignment2.grade = 70
        self.student.submit_assignment(assignment2)
        assignment3 = cm.Assignment('assignment3', 60)
        assignment3.grade = 50
        self.student.submit_assignment(assignment3)
        avg = assignment2.grade + assignment3.grade
        avg /= 2.0
        self.assertEqual(avg, self.student.get_average())

    def testRemoveAssignment(self):
        self.student.submit_assignment(self.assignment)
        self.student.submit_assignment(cm.Assignment('assignment', 100))
        self.student.submit_assignment(cm.Assignment('assignment', 100))
        count = len(self.student.get_assignments())
        self.student.remove_assignment('assignment')
        count -= 1
        self.assertEqual(count, len(self.student.assignments))


class TestAssignment(TestCase):

    def setUp(self):
        self.assignment = cm.Assignment('Test Assignment', 100)

    def testAssignmentInit(self):
        self.assertEqual(self.assignment.name, 'Test Assignment')
        self.assertEqual(self.assignment.max_score, 100)
        self.assertEqual(self.assignment.grade, None)

    def testAssignGrade(self):
        self.assignment.assign_grade(110)
        self.assertIsNone(self.assignment.grade)