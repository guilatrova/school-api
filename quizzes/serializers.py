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

        if self._has_answer_duplicates(answers, lambda x: x['choice']):
            raise serializers.ValidationError("Choices can't repeat")

        if self._has_answer_duplicates(answers, lambda x: x['description'].lower().strip()):
            raise serializers.ValidationError("Answers can't repeat")

        return answers

    def _has_answer_duplicates(self, answers, getter):
        check = set()
        for answer in answers:
            check.add(getter(answer))
        
        return len(check) != 4