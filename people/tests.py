from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import reverse
from people import views, serializers
from people.models import Student, Teacher
from common.tests.mixins import UrlTestMixin, ApiTestMixin

class StudentUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'students'
    single_name = 'student'
    view = views.StudentViewSet

class TeacherUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'teachers'
    single_name = 'teacher'
    view = views.TeacherViewSet

class StudentSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        data = { 'name': 'Jhon Doe' }
        serializer = serializers.StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class TestSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        data = { 'name': 'Anakin Skywalker' }
        serializer = serializers.TeacherSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class StudentApiIntegrationTestCase(ApiTestMixin, APITestCase):
    model = Student
    post_data = { 'name': 'Jhon Doe' }

    @property
    def update_data(self):
        return { 'id': self.pre_created_entity.id, 'name': 'Changed' }

    @classmethod
    def setUpTestData(cls):
        cls.pre_created_entity = Student.objects.create(name='Jhon Doe')

    def setUp(self):
        self.list_url = reverse('students')
        self.single_url = reverse('student', kwargs={'pk': self.pre_created_entity.id})

class TeacherApiIntegrationTestCase(ApiTestMixin, APITestCase):
    model = Teacher
    post_data = { 'name': 'Guilherme Latrova' }

    @property
    def update_data(self):
        return { 'id': self.pre_created_entity.id, 'name': 'Changed' }

    @classmethod
    def setUpTestData(cls):
        cls.pre_created_entity = Teacher.objects.create(name='Jhon Doe')

    def setUp(self):
        self.list_url = reverse('teachers')
        self.single_url = reverse('teacher', kwargs={'pk': self.pre_created_entity.id})