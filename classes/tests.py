from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from people.models import Teacher
from classes import views, serializers
from classes.models import Class
from common.tests.mixins import UrlTestMixin, ApiTestMixin

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

class ClassApiIntegrationTestCase(SetupTeacherDataMixin, ApiTestMixin, APITestCase):
    model = Class    

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pre_created_entity = Class.objects.create(name='Python with TDD', teacher=cls.teacher)

    def setUp(self):
        self.list_url = reverse('classes')
        self.single_url = reverse('class', kwargs={'pk': self.pre_created_entity.id})

    @property
    def post_data(self):
        return { 'name': 'Testing APIs', 'teacher': self.teacher.id }

    @property
    def update_data(self):
        return { 'id': self.pre_created_entity.id, 'name': 'Changed', 'teacher': self.teacher.id }