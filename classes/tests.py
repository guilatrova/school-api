from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from people.models import Teacher
from classes import views, serializers
from classes.models import Class
from common.tests.mixins import UrlTestMixin

class ClassesUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'classes'
    single_name = 'class'
    view = views.ClassViewSet

class SetupTeacherDataMixin:
    @classmethod
    def setUpTestData(cls):
        cls.teacher = Teacher.objects.create(name='Guilherme Latrova')

class ClassSerializerTestCase(SetupTeacherDataMixin, TestCase):
    def test_serializer_validates(self):
        data = { 'name': 'Python with TDD', 'teacher': self.teacher.id }
        serializer = serializers.ClassSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class ClassApiIntegrationTestCase(SetupTeacherDataMixin, TestCase):
    def test_creates_class(self):
        data = { 'name': 'Python with TDD', 'teacher': self.teacher.id }

        response = self.client.post(reverse('classes'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Class.objects.count(), 1)