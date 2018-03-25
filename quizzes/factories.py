from .models import Quiz, Question, Answer, Assignment
from classes.models import SchoolClass

def create_quiz(validated_data):
    questions = validated_data.pop('questions')
    quiz = Quiz.objects.create(**validated_data)

    for question_data in questions:
        answers = question_data.pop('answers')
        question = Question.objects.create(quiz=quiz, **question_data)

        for answer_data in answers:
            Answer.objects.create(question=question, **answer_data)

    return quiz

class GradeByClassReport:
    def __init__(self, teacher_id):
        self.teacher_id = teacher_id

    def generate(self):
        data = self._get_data()
        return self._prep_data(data)     

    def _get_data(self):
        return SchoolClass.objects.filter(
            teacher=self.teacher_id
        )

    def _prep_data(self, data):
        lst = []
        for entry in data:
            lst.append(entry.name)
        return lst