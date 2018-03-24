from django.urls import path
from quizzes import views

list_actions = { 'get': 'list', 'post': 'create' }
single_actions = { 'get': 'retrieve' }

urlpatterns = [
    path('', views.QuizViewSet.as_view(list_actions), name='quizzes'),
    path('<int:pk>/', views.QuizViewSet.as_view(single_actions), name='quiz')
]