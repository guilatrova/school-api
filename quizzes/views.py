from django.shortcuts import render
from rest_framework import viewsets
from .serializers import QuizSerializer

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer