from django.db.models import F, Sum
from itertools import groupby
from .models import Quiz, Question, Answer, Assignment
from classes.models import SchoolClass, StudentEnrollment

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
    def __init__(self, teacher_id, semester):
        self.teacher_id = teacher_id
        self.semester = semester

    def generate(self):
        data = self._get_data()
        return self._prep_data(data)     

    def _get_data(self):
        queryset = SchoolClass.objects.filter(teacher_id=self.teacher_id)
        return queryset\
                    .values('studentenrollment')\
                    .annotate(
                        class_name=F('studentenrollment__school_class__name'),
                        student_name=F('studentenrollment__student__name'),
                        grade=Sum('studentenrollment__assignment__grade')
                    )\
                    .order_by('class_name')

    def _prep_data(self, data):
        class_group = {}
        for key, group in groupby(data, lambda x: x['class_name']):
            class_group[key] = (list(group))

        result = {}
        for school_class in class_group:
            result[school_class] = {}
            for student in class_group[school_class]:
                result[school_class][student['student_name']] = student['grade']

        return result