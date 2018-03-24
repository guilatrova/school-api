from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from quizzes import views, serializers, factories
from quizzes.models import Quiz, Question, Answer
from people.models import Teacher, Student
from classes.models import SchoolClass
from common.tests.mixins import UrlTestMixin

def create_questions(how_many):
    answers = create_answers('A', 'B', 'C', 'D')
    return [create_question(answers) for x in range(how_many)]

def create_question(answers):
    return {
        'description': 'question',
        'correct_answer': 1,
        'answers': answers
    }

def create_answers(*args):
    lst = []
    for i in range(len(args)):
        description = args[i]
        choice = i + 1
        lst.append({ 'choice': choice, 'description': description })

    return lst

class SetupSchoolClassDataMixin:
    @classmethod
    def setUpTestData(cls):
        teacher = Teacher.objects.create(name='Guilherme Latrova')
        cls.school_class = SchoolClass.objects.create(name='QA', teacher=teacher)

class QuizUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'quizzes'
    single_name = 'quiz'
    allowed_single = ['get']
    allowed_list = ['get', 'post']
    view = views.QuizViewSet

class AnswerSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        data = { 'choice': 1, 'description': 'answer' }
        serializer = serializers.AnswerSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

class QuestionSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        answers_data = create_answers('django', 'flask', 'cherry', 'none')
        question_data =  question_data =  create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_answer_validates_should_have_4_answers_choices(self):
        answers_data = create_answers('just', 'three', 'answers')
        question_data =  create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def test_answer_validates_should_not_allows_repetead_choices(self):
        answers_data = create_answers('yes', 'no', 'well...', 'I dont know')
        answers_data[1]['choice'] = 'A' #now we got two A choices
        question_data = create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def test_answer_validates_should_not_allows_repeated_answers(self):
        answers_data = create_answers('same', 'same', 'other', 'one more')
        question_data = create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def assert_has_error(self, serializer, key):
        self.assertFalse(serializer.is_valid())
        self.assertIn(key, serializer.errors)

class QuizSerializerTestCase(SetupSchoolClassDataMixin, TestCase):
    def test_serializer_validates(self):
        answers_data = create_answers('A', 'B', 'C', 'D')
        questions_data = [create_question(answers_data) for x in range(3)]
        data = { 'school_class': self.school_class.id, 'questions': questions_data }

        serializer = serializers.QuizSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    @patch('quizzes.factories.create_quiz', return_value=MagicMock())
    def test_serializer_creates(self, mock):
        answers_data = create_answers('A', 'B', 'C', 'D')
        questions_data = [create_question(answers_data) for x in range(3)]
        data = { 'school_class': self.school_class.id, 'questions': questions_data }

        serializer = serializers.QuizSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()

        self.assertTrue(mock.called)
        self.assert_called_with_one_arg(mock)

    def assert_called_with_one_arg(self, mock):
        first_call = mock.call_args_list[0]
        args, kwargs = first_call
        self.assertEqual(len(args), 1)

class AssignmentSerializerTestCase(SetupSchoolClassDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.quiz = factories.create_quiz({ 'school_class': cls.school_class, 'questions': create_questions(2) })
        cls.student = Student.objects.create(name='Jhon Doe')

    def test_serializer_validates(self):
        data = { 'quiz': self.quiz.id, 'student': self.student.id }
        serializer = serializers.AssignmentSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

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

class QuizApiIntegrationTestCase(SetupSchoolClassDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.quiz = factories.create_quiz({ 'school_class': cls.school_class, 'questions': create_questions(2) })

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