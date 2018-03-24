from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SchoolClassSerializer, StudentEnrollmentSerializer
from .models import SchoolClass, StudentEnrollment

class SchoolClassViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolClassSerializer
    queryset = SchoolClass.objects.all()

class StudentClassesViewSet(viewsets.ModelViewSet):
    serializer_class = StudentEnrollmentSerializer

    def get_queryset(self):
        student_id = self.kwargs['pk']
        return StudentEnrollment.objects.filter(student_id=student_id)