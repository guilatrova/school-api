from django.test import TestCase
from django.urls import reverse, resolve
from people import views

class PeopleUrl(TestCase):
    def test_resolves_students_list_url(self):
        resolver = resolve(reverse('students'))
        self.assertEqual(resolver.func.cls, views.StudentViewSet)