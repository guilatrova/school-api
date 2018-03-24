from rest_framework import serializers
from classes.models import SchoolClass

class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ('id', 'name', 'teacher')