from django.test import TestCase
from django.urls import reverse, resolve
from people import views

def resolve_by_name(name, **kwargs):
    url = reverse(name, kwargs=kwargs)
    return resolve(url)

class PeopleUrl(TestCase):
    def test_resolves_students_list_url(self):
        resolver = resolve_by_name('students')
        self.assertEqual(resolver.func.cls, views.StudentViewSet)

    def test_resolves_students_single_url(self):
        resolver = resolve_by_name('student', id=1)
        self.assertEqual(resolver.func.cls, views.StudentViewSet)

    