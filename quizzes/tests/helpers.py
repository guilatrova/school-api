from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from quizzes.models import Assignment
from quizzes import factories

class SetupSchoolClassDataMixin:
    @classmethod
    def setUpTestData(cls):
        teacher = Teacher.objects.create(name='Guilherme Latrova')
        cls.school_class = SchoolClass.objects.create(name='QA', teacher=teacher)

class SetupQuizDataMixin(SetupSchoolClassDataMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.quiz = factories.create_quiz({ 'school_class': cls.school_class, 'questions': create_questions(2) })

class SetupStudentEnrollmentDataMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.student = Student.objects.create(name='Jhon Doe')
        cls.enrollment = StudentEnrollment.objects.create(student=cls.student, school_class=cls.school_class)

class SetupAssignmentDataMixin(SetupStudentEnrollmentDataMixin, SetupQuizDataMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.assignment = Assignment.objects.create(quiz=cls.quiz, enrollment=cls.enrollment)

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