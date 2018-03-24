from django.test import TestCase
from django.urls import reverse, resolve
from people.models import Teacher
from classes import views, serializers
from common.tests.mixins import UrlTestMixin

class ClassesUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'classes'
    single_name = 'class'
    view = views.ClassViewSet

class ClassSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = Teacher.objects.create(name='Guilherme Latrova')

    def test_serializer_validates(self):
        data = { 'name': 'Python with TDD', 'teacher': self.teacher }
        serializer = serializers.ClassSerializer(data=data)
        self.assertTrue(serializer.is_valid())