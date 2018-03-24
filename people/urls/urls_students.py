from django.urls import path
from people import views
from classes import views as classes_views

list_actions = { 'get': 'list', 'post': 'create' }
single_actions = { 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' }
classes_action = { 'get': 'list', 'post': 'create' }

urlpatterns = [
    path('', views.StudentViewSet.as_view(list_actions), name='students'),
    path('<int:pk>/', views.StudentViewSet.as_view(single_actions), name='student'),
    path('<int:pk>/classes', classes_views.StudentClassesViewSet.as_view(classes_action), name='student-classes'),
]