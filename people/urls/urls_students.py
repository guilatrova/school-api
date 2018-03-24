from django.urls import path
from people import views

list_actions = { 'get': 'list', 'post': 'create' }
single_actions = { 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' }

urlpatterns = [
    path('', views.StudentViewSet.as_view(list_actions), name='students'),
    path('<int:pk>/', views.StudentViewSet.as_view(single_actions), name='student')
]