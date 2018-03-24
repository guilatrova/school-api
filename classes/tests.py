from django.test import TestCase
from django.urls import reverse, resolve
from classes import views
from common.tests.mixins import UrlTestMixin

class ClassesUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'classes'
    single_name = 'class'
    view = views.ClassViewSet