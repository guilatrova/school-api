from django.shortcuts import render
from rest_framework import viewsets
from .serializers import QuizSerializer
from .models import Quiz

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()