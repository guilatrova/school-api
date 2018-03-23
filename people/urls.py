from django.urls import path
from people import views

urlpatterns = [
    path('', views.StudentViewSet.as_view({ 'get': 'list' }), name='students')
]