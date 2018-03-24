from django.urls import path
from classes import views

list_actions = { 'get': 'list' }

urlpatterns = [
    path('', views.ClassViewSet.as_view(list_actions), name='classes'),
]