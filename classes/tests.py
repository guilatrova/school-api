from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from people.models import Teacher, Student
from classes import views, serializers
from classes.models import SchoolClass, StudentEnrollment
from common.tests.mixins import UrlTestMixin, ApiTestMixin

class SchoolClassUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'classes'
    single_name = 'class'
    view = views.SchoolClassViewSet

class SetupTeacherDataMixin:
    @classmethod
    def setUpTestData(cls):
        cls.teacher = Teacher.objects.create(name='Guilherme Latrova')

class SchoolClassSerializerTestCase(SetupTeacherDataMixin, TestCase):
    def test_serializer_validates(self):
        data = { 'name': 'Python with TDD', 'teacher': self.teacher.id }
        serializer = serializers.SchoolClassSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class StudentEnrollmentSerializerTestCase(SetupTeacherDataMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.school_class = SchoolClass.objects.create(name='Python with TDD', teacher=cls.teacher)
        cls.student = Student.objects.create(name='Jhon Doe')

    def test_serializer_validates(self):
        data = { 'school_class': self.school_class.id, 'student': self.student.id }
        serializer = serializers.StudentEnrollmentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

class ClassApiIntegrationTestCase(SetupTeacherDataMixin, ApiTestMixin, APITestCase):
    model = SchoolClass

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pre_created_entity = SchoolClass.objects.create(name='Python with TDD', teacher=cls.teacher)

    def setUp(self):
        self.list_url = reverse('classes')
        self.single_url = reverse('class', kwargs={'pk': self.pre_created_entity.id})

    @property
    def post_data(self):
        return { 'name': 'Testing APIs', 'teacher': self.teacher.id }

    @property
    def update_data(self):
        return { 'id': self.pre_created_entity.id, 'name': 'Changed', 'teacher': self.teacher.id }

class StudentClassesApiIntegrationTestCase(SetupTeacherDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.school_class = SchoolClass.objects.create(name='class', teacher=cls.teacher)
        cls.student = Student.objects.create(name='Jhon Doe')
        cls.enrollment = StudentEnrollment(student=cls.student, school_class=cls.school_class)

    def test_creates_enrollment(self):
        data = { 'student': self.student.id, 'school_class': self.school_class.id }
        url = reverse('student-classes', kwargs={'pk': self.student.id})

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentEnrollment.objects.count(), 1)

