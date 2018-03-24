from django.test import TestCase
from django.urls import reverse, resolve
from classes import views

class ClassesUrlsTestCase(TestCase):
    def test_resolves_list_url(self):
        resolver = self.resolve_by_name('classes')
        self.assertEqual(resolver.func.cls, views.ClassViewSet)

    def resolve_by_name(self, name, **kwargs):
        url = reverse(name, kwargs=kwargs)
        return resolve(url)