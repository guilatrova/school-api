from django.test import TestCase
from quizzes import views, serializers, factories
from quizzes.models import Quiz, Question, Answer, Assignment
from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from common.tests.mixins import UrlTestMixin
from .helpers import SetupSchoolClassDataMixin, create_questions, create_question, create_answers

class QuizUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'quizzes'
    single_name = 'quiz'
    allowed_single = ['get']
    view = views.QuizViewSet

class AssignmentUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'assignments'
    single_name = 'assignment'
    allowed_single = ['get']
    allowed_list = ['get']
    view = views.AssignmentViewSet

# class SubmissionUrlsTestCase(UrlTestMixin, TestCase):
#     list_name = 'assignment-submissions'
#     allowed_list = ['get', 'post']

class FactoriesTestCase(SetupSchoolClassDataMixin, TestCase):
    def setUp(self):
        answers = create_answers('A', 'B', 'C', 'D')
        questions = [create_question(answers) for x in range(3)]
        self.data = {
            'school_class': self.school_class,
            'questions': questions
        }

    def test_create_quiz(self):
        factories.create_quiz(self.data)

        self.assertEqual(Answer.objects.count(), 4 * 3)
        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Quiz.objects.count(), 1)

