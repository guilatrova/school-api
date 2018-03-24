from django.shortcuts import render
from rest_framework import viewsets
from .serializers import QuizSerializer
from .models import Quiz

class QuizViewSet(mixins.CreateModelMixin, 
                  mixins.ListModelMixin, 
                  viewsets.GenericViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

class StudentAssignmentsViewSet(viewsets.ModelViewSet):
    pass