from django.shortcuts import render
from rest_framework import viewsets, mixins
from .serializers import QuizSerializer, AssignmentSerializer
from .models import Quiz

class QuizViewSet(mixins.CreateModelMixin, 
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

class StudentAssignmentsViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer