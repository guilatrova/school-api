from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment

class SetupSchoolClassDataMixin:
    @classmethod
    def setUpTestData(cls):
        teacher = Teacher.objects.create(name='Guilherme Latrova')
        cls.school_class = SchoolClass.objects.create(name='QA', teacher=teacher)

def create_questions(how_many):
    answers = create_answers('A', 'B', 'C', 'D')
    return [create_question(answers) for x in range(how_many)]

def create_question(answers):
    return {
        'description': 'question',
        'correct_answer': 1,
        'answers': answers
    }

def create_answers(*args):
    lst = []
    for i in range(len(args)):
        description = args[i]
        choice = i + 1
        lst.append({ 'choice': choice, 'description': description })

    return lst