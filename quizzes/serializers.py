from rest_framework import serializers
from quizzes import factories
from .models import Answer, Question, Quiz, Assignment

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('description', 'choice')

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = Question
        fields = ('id', 'description', 'answers', 'correct_answer')

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

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'school_class', 'questions')

    def create(self, validated_data):
        return factories.create_quiz(validated_data)

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'quiz', 'enrollment')