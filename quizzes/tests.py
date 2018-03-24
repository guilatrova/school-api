from django.test import TestCase
from unittest.mock import patch
from quizzes import views, serializers
from people.models import Teacher
from classes.models import SchoolClass
from common.tests.mixins import UrlTestMixin

def create_question(answers):
    return {
        'description': 'question',
        'correct_answer': 'D',
        'answers': answers
    }

def create_answers(*args):
    lst = []
    for i in range(len(args)):
        description = args[i]
        choice = chr(65 + i)
        lst.append({ 'choice': choice, 'description': description })

    return lst

class QuizUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'quizzes'
    single_name = 'quiz'
    view = views.QuizViewSet

class AnswerSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        data = { 'choice': 'A', 'description': 'answer' }
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

class QuizSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        teacher = Teacher.objects.create(name='Guilherme Latrova')
        cls.school_class = SchoolClass.objects.create(name='QA', teacher=teacher)

    def test_serializer_validates(self):
        answers_data = create_answers('A', 'B', 'C', 'D')
        questions_data = [create_question(answers_data) for x in range(3)]
        data = { 'school_class': self.school_class.id, 'questions': questions_data }

        serializer = serializers.QuizSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    @patch('quizzes.factories.QuizFactory.create')
    def test_serializer_creates(self, mock):
        answers_data = create_answers('A', 'B', 'C', 'D')
        questions_data = [create_question(answers_data) for x in range(3)]
        data = { 'school_class': self.school_class.id, 'questions': questions_data }

        serializer = serializers.QuizSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(mock.called)
