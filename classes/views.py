from django.shortcuts import render
from rest_framework import viewsets, mixins
from .serializers import SchoolClassSerializer, StudentEnrollmentSerializer
from .models import SchoolClass, StudentEnrollment

class SchoolClassViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolClassSerializer
    queryset = SchoolClass.objects.all()

class StudentClassesViewSet(mixins.CreateModelMixin, 
                            mixins.ListModelMixin, 
                            viewsets.GenericViewSet):
    """
    A viewset that only handles Create and List 
    for student enrollment in classes.
    """
    serializer_class = StudentEnrollmentSerializer

    def get_queryset(self):
        return StudentEnrollment.objects.filter(student_id=self.kwargs['student_id'])