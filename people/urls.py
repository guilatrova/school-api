from django.urls import path
from people import views

urlpatterns = [
    path('', views.StudentViewSet.as_view({ 'get': 'list' }), name='students'),
    path('<int:id>/', views.StudentViewSet.as_view({ 'get': 'retrieve' }), name='student')
]