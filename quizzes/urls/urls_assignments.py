from django.urls import path
from quizzes import views

list_actions = { 'get': 'list' }
single_actions = { 'get': 'retrieve' }

urlpatterns = [
    path('', views.AssignmentViewSet.as_view(list_actions), name='assignments'),
    path('<int:pk>/', views.AssignmentViewSet.as_view(single_actions), name='assignment'),
]