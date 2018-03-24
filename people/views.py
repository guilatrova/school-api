from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StudentSerializer, TeacherSerializer
from .models import Student, Teacher

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()