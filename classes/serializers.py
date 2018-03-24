from rest_framework import serializers
from classes.models import SchoolClass, StudentEnrollment

class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ('id', 'name', 'teacher')

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = ('id', 'student', 'school_class')