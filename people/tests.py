from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse, resolve
from people import views, serializers, models

class StudentUrlsTestCase(TestCase):
    def test_resolves_students_list_url(self):
        resolver = self.resolve_by_name('students')
        self.assertEqual(resolver.func.cls, views.StudentViewSet)

    def test_resolves_students_single_url(self):
        resolver = self.resolve_by_name('student', id=1)
        self.assertEqual(resolver.func.cls, views.StudentViewSet)

    def test_students_list_url_allows(self):
        resolver = self.resolve_by_name('students')
        allowed = ['get', 'post']
        self.assert_has_actions(allowed, resolver.func.actions)

    def test_students_single_url_allows(self):
        resolver = self.resolve_by_name('student', id=1)
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
    def test_creates_student(self):
        data = { 'name': 'Jhon Doe' }
        url = reverse('students')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Student.objects.count(), 1)

    def test_lists_students(self):
        models.Student.objects.create(name='Jhon Doe')
        url = reverse('students')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)