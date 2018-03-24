from .models import Quiz, Question, Answer

def create_quiz(validated_data):
    questions = validated_data.pop('questions')
    quiz = Quiz.objects.create(**validated_data)

    for question_data in questions:
        answers = question_data.pop('answers')
        question = Question.objects.create(quiz=quiz, **question_data)

        for answer_data in answers:
            Answer.objects.create(question=question, **answer_data)

    return quiz