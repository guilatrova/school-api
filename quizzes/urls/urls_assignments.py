from django.urls import path
from quizzes import views

list_actions = { 'get': 'list' }
single_actions = { 'get': 'retrieve' }
submission_actions = { 'get': 'list', 'post': 'create' }

urlpatterns = [
    path('', views.AssignmentViewSet.as_view(list_actions), name='assignments'),
    path('<int:pk>/', views.AssignmentViewSet.as_view(single_actions), name='assignment'),
    path('<int:assignment_id>/submissions/', views.SubmissionViewSet.as_view(submission_actions), name='assignment-submissions'),
]