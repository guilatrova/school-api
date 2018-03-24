from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ClassSerializer
from .models import Class

class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSerializer
    queryset = Class.objects.all()