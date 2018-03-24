from django.test import TestCase
from quizzes import views
from common.tests.mixins import UrlTestMixin

class QuizUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'quizzes'
    single_name = 'quiz'
    view = views.QuizViewSet