from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ClassSerializer

class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSerializer