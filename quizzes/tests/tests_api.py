from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from quizzes.models import Quiz, Question, Answer, Assignment
from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from quizzes import factories
from .helpers import SetupSchoolClassDataMixin, create_questions

class SetupQuizDataMixin(SetupSchoolClassDataMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.quiz = factories.create_quiz({ 'school_class': cls.school_class, 'questions': create_questions(2) })

class QuizApiIntegrationTestCase(SetupQuizDataMixin, APITestCase):
    def setUp(self):
        self.questions = create_questions(4)

    def test_api_creates_complete_quiz(self):
        data = {
            'school_class': self.school_class.id,
            'questions': self.questions
        }

        response = self.client.post(reverse('quizzes'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)

    def test_api_retrieves_quiz(self):
        response = self.client.get(reverse('quiz', kwargs={'pk': self.quiz.id}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.quiz.id)

    def test_api_lists_quizzes(self):
        response = self.client.get(reverse('quizzes'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class StudentAssignmentApiIntegrationTestCase(SetupQuizDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.student = Student.objects.create(name='Jhon Doe')
        cls.enrollment = StudentEnrollment.objects.create(student=cls.student, school_class=cls.school_class)
        cls.assignment = Assignment.objects.create(quiz=cls.quiz, enrollment=cls.enrollment)

        other_student = Student.objects.create(name='Mary Doe') #Make sure only student's assignments are handled
        other_enrollment = StudentEnrollment.objects.create(student=other_student, school_class=cls.school_class)
        Assignment.objects.create(quiz=cls.quiz, enrollment=other_enrollment)

    def test_api_creates_assignment(self):
        data = {
            'quiz': self.quiz.id,
            'enrollment': self.enrollment.id
        }
        url = reverse('student-assignments', kwargs={'student_id': self.student.id})

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 3)

    def test_api_lists_assignments(self):
        url = reverse('student-assignments', kwargs={'student_id': self.student.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class AssignmentApiIntegrationTestCase(SetupQuizDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.student = Student.objects.create(name='Jhon Doe')
        cls.enrollment = StudentEnrollment.objects.create(student=cls.student, school_class=cls.school_class)
        cls.assignment = Assignment.objects.create(quiz=cls.quiz, enrollment=cls.enrollment)

    def test_api_retrieves_assignment(self):
        url = reverse('assignment', kwargs={'pk': self.assignment.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.assignment.id)