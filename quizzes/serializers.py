from rest_framework import serializers
from .models import Answer, Question

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('description', 'choice')

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ('id', 'description', 'answers')