from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from people import views, serializers
from people.models import Student, Teacher
from common.tests.mixins import UrlTestMixin

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

class ApiTestMixin:
    def test_creates_student(self):
        data = { 'name': 'Jhon Doe' }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), 2)

    def test_lists(self):
        response = self.client.get(self.list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update(self):
        id = self.pre_created_entity.id
        data = { 'pk': id, 'name': 'Changed' }

        response = self.client.put(self.single_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pre_created_entity.refresh_from_db()
        self.assertEqual(self.pre_created_entity.name, data['name'])

    def test_retrieves(self):
        response = self.client.get(self.single_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.pre_created_entity.name)

    def test_deletes(self):
        response = self.client.delete(self.single_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.model.objects.count(), 0)

class StudentApiIntegrationTestCase(ApiTestMixin, APITestCase):
    model = Student

    @classmethod
    def setUpTestData(cls):
        cls.pre_created_entity = Student.objects.create(name='Jhon Doe')

    def setUp(self):
        self.list_url = reverse('students')
        self.single_url = reverse('student', kwargs={'pk': self.pre_created_entity.id})

class TeacherApiIntegrationTestCase(ApiTestMixin, APITestCase):
    model = Teacher

    @classmethod
    def setUpTestData(cls):
        cls.pre_created_entity = Teacher.objects.create(name='Jhon Doe')

    def setUp(self):
        self.list_url = reverse('teachers')
        self.single_url = reverse('teacher', kwargs={'pk': self.pre_created_entity.id})