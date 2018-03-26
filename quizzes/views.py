from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .serializers import QuizSerializer, AssignmentSerializer, SubmissionSerializer
from .models import Quiz, Assignment, Submission
from quizzes import factories

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

    def get_serializer_context(self):
        return { 'assignment_id': self.kwargs['assignment_id'] }

    def perform_create(self, serializer):
        serializer.save(assignment_id=self.kwargs['assignment_id'])

@api_view()
def get_grade_report(request):
    teacher = request.GET.get('teacher')
    if (teacher is None):
        raise MissingParams()

    data = factories.GradeByClassReport(teacher).generate()
    return Response(data)

class MissingParams(APIException):
    status_code = 422
    default_detail = 'There are missing required query params to handle request.'
    default_code = 'missing_params'