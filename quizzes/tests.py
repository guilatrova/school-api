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