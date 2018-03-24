from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse, resolve
from people import views, serializers
from people.models import Student

class StudentUrlsTestCase(TestCase):
    def test_resolves_students_list_url(self):
        resolver = self.resolve_by_name('students')
        self.assertEqual(resolver.func.cls, views.StudentViewSet)

    def test_resolves_students_single_url(self):
        resolver = self.resolve_by_name('student', pk=1)
        self.assertEqual(resolver.func.cls, views.StudentViewSet)

    def test_students_list_url_allows(self):
        resolver = self.resolve_by_name('students')
        allowed = ['get', 'post']
        self.assert_has_actions(allowed, resolver.func.actions)

    def test_students_single_url_allows(self):
        resolver = self.resolve_by_name('student', pk=1)
        allowed = ['get', 'put', 'delete']
        self.assert_has_actions(allowed, resolver.func.actions)

    def resolve_by_name(self, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)

    def assert_has_actions(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for action in expected:
            self.assertIn(action, actual)

class StudentSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        data = { 'name': 'Jhon Doe' }
        serializer = serializers.StudentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class StudentApiIntegrationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pre_created_student = Student.objects.create(name='Jhon Doe')

    def setUp(self):
        self.list_url = reverse('students')
        self.single_url = reverse('student', kwargs={'pk': self.pre_created_student.id})

    def test_creates_student(self):
        data = { 'name': 'Jhon Doe' }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_lists_students(self):
        response = self.client.get(self.list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_student(self):
        id = self.pre_created_student.id
        data = { 'pk': id, 'name': 'Changed' }
        
        response = self.client.put(self.single_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pre_created_student.refresh_from_db()
        self.assertEqual(self.pre_created_student.name, data['name'])