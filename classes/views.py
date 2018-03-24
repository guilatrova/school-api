from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SchoolClassSerializer, StudentEnrollmentSerializer
from .models import SchoolClass

class SchoolClassViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolClassSerializer
    queryset = SchoolClass.objects.all()

class StudentClassesViewSet(viewsets.ModelViewSet):
    serializer_class = StudentEnrollmentSerializer