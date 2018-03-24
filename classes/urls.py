from django.urls import path
from classes import views

list_actions = { 'get': 'list', 'post': 'create' }
single_actions = { 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' }

urlpatterns = [
    path('', views.ClassViewSet.as_view(list_actions), name='classes'),
    path('<int:pk>/', views.ClassViewSet.as_view(single_actions), name='class')
]