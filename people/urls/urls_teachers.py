from django.urls import path
from people import views

list_actions = { 'get': 'list', 'post': 'create' }
single_actions = { 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' }

urlpatterns = [
    path('', views.TeacherViewSet.as_view(list_actions), name='teachers'),
    path('<int:pk>/', views.TeacherViewSet.as_view(single_actions), name='teacher')
]