from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from django.urls import reverse
from quizzes.models import Quiz, Question, Answer, Assignment, Submission
from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from quizzes import factories
from .helpers import (
    SetupQuizDataMixin,
    SetupAssignmentDataMixin,
    create_questions
)

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

class StudentAssignmentApiIntegrationTestCase(SetupAssignmentDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        other_student = Student.objects.create(name='Mary Doe') #Make sure only student's assignments are handled
        other_enrollment = StudentEnrollment.objects.create(student=other_student, school_class=cls.school_class, semester=date(2018, 1, 1))
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

class AssignmentApiIntegrationTestCase(SetupAssignmentDataMixin, APITestCase):
    def test_api_retrieves_assignment(self):
        url = reverse('assignment', kwargs={'pk': self.assignment.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.assignment.id)

    def test_api_lists_assignments(self):
        url = reverse('assignments')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class SubmissionApiIntegrationTestCase(SetupAssignmentDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Submission.objects.create(assignment=cls.assignment, question=cls.quiz.questions.first(), answer=1)
        #Make sure it only returns from specified assignment
        other_quiz = factories.create_quiz({ 'school_class': cls.school_class, 'questions': create_questions(1) })
        other_assignment = Assignment.objects.create(quiz=other_quiz, enrollment=cls.enrollment)
        Submission.objects.create(assignment=other_assignment, question=other_quiz.questions.first(), answer=1)

    def test_api_creates_submission(self):
        data = { 'question': self.quiz.questions.last().id, 'answer': 1 }
        url = reverse('assignment-submissions', kwargs={'assignment_id': self.assignment.id})

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Submission.objects.count(), 3)

    def test_api_lists_submission(self):
        url = reverse('assignment-submissions', kwargs={'assignment_id': self.assignment.id})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class GradeReportApiTestCase(APITestCase):

    @patch('quizzes.factories.GradeByClassReport.generate', return_value=[])
    def test_api_returns_report_results(self, mock):
        url = reverse('student-grades-report') + "?teacher=1"
        response = self.client.get(url, format='json')

        self.assertTrue(mock.called)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    @patch('quizzes.factories.GradeByClassReport', return_value=MagicMock(generate=lambda : []))
    def test_api_pass_data_to_report(self, mock):
        url = reverse('student-grades-report') + "?teacher=1"
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock.assert_called_with('1')

    def test_api_should_reject_calls_without_teacher_specified(self):
        url = reverse('student-grades-report')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)