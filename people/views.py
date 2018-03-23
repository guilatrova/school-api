from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer