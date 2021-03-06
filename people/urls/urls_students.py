from django.urls import path
from people import views
from classes import views as classes_views
from quizzes import views as quizzes_views

list_actions = { 'get': 'list', 'post': 'create' }
single_actions = { 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' }
relation_actions = { 'get': 'list', 'post': 'create' }

urlpatterns = [
    path('', views.StudentViewSet.as_view(list_actions), name='students'),
    path('<int:pk>/', views.StudentViewSet.as_view(single_actions), name='student'),
    path('<int:student_id>/classes', classes_views.StudentClassesViewSet.as_view(relation_actions), name='student-classes'),
    path('<int:student_id>/assignments', quizzes_views.StudentAssignmentsViewSet.as_view(relation_actions), name='student-assignments'),
]