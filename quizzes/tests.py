from django.test import TestCase
from quizzes import views, serializers
from people.models import Teacher
from common.tests.mixins import UrlTestMixin

class QuizUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'quizzes'
    single_name = 'quiz'
    view = views.QuizViewSet

class AnswerSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        data = { 'choice': 'A', 'description': 'answer' }
        serializer = serializers.AnswerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class QuestionSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        answers_data = self.create_answers('django', 'flask', 'cherry', 'none')
        question_data =  question_data =  self.create_question(answers_data)
        
        serializer = serializers.QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid())

    def test_answer_validates_should_have_4_answers_choices(self):
        answers_data = self.create_answers('just', 'three', 'answers')
        question_data =  self.create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def test_answer_validates_should_not_allows_repetead_choices(self):
        answers_data = self.create_answers('yes', 'no', 'well...', 'I dont know')
        answers_data[1]['choice'] = 'A' #now we got two A choices
        question_data = self.create_question(answers_data)
        
        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def assert_has_error(self, serializer, key):
        self.assertFalse(serializer.is_valid())
        self.assertIn(key, serializer.errors)

    def create_question(self, answers):
        return {
            'description': 'question',
            'correct_answer': 'D',
            'answers': answers
        }

    def create_answers(self, *args):
        lst = []
        for i in range(len(args)):
            description = args[i]
            choice = chr(65 + i)
            lst.append({ 'choice': choice, 'description': description })

        return lst

# DO LATER
# class QuizSerializerTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.teacher = Teacher.objects.create(name='Guilherme Latrova')

#     def test_serializer_validates(self):
#         questions_data = [
#             'description': 'Which one is the best framework for perfectionists?',
#             'correct_answer': 'A',
#             'answers': [
#                 {
#                     'choice': 'A',
#                     'description': ''                    
#                 }
#             ]
#         ]
#         data = { 'teacher': self.teacher.id, 'questions' }