from django.urls import path
from people import views

urlpatterns = [
    path('', views.StudentViewSet.as_view({ 'get': 'list', 'post': 'create' }), name='students'),
    path('<int:id>/', views.StudentViewSet.as_view({ 'get': 'retrieve', 'put': 'update', 'delete': 'destroy' }), name='student')
]