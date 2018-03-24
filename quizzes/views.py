from django.shortcuts import render
from rest_framework import viewsets, mixins
from .serializers import QuizSerializer, AssignmentSerializer
from .models import Quiz, Assignment

class QuizViewSet(mixins.CreateModelMixin, 
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

class StudentAssignmentsViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    
    def get_queryset(self):
        return Assignment.objects.filter(enrollment__student_id=self.kwargs['student_id'])