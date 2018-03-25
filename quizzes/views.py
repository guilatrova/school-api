from django.shortcuts import render
from rest_framework import viewsets, mixins
from .serializers import QuizSerializer, AssignmentSerializer, SubmissionSerializer
from .models import Quiz, Assignment, Submission

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

class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(assignment_id=self.kwargs['assignment_id'])

    def perform_create(self, serializer):
        serializer.save(assignment_id=self.kwargs['assignment_id'])