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

    def validate_answers(self, answers):
        if len(answers) != 4:
            raise serializers.ValidationError('Question should have exactly 4 answer choices')

        choices = set()
        for answer in answers:
            choices.add(answer['choice'])

        if len(choices) != 4:
            raise serializers.ValidationError("Choices can't repeat")

        return answers