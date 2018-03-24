from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from quizzes.models import Quiz, Question, Answer, Assignment
from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from quizzes import factories

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

class QuizApiIntegrationTestCase(SetupSchoolClassDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.quiz = factories.create_quiz({ 'school_class': cls.school_class, 'questions': create_questions(2) })

    def setUp(self):
        self.questions = create_questions(4)

    def test_api_creates_complete_quiz(self):
        data = {
            'school_class': self.school_class.id,
            'questions': self.questions
        }

        response = self.client.post(reverse('quizzes'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)

    def test_api_retrieves_quiz(self):
        response = self.client.get(reverse('quiz', kwargs={'pk': self.quiz.id}), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.quiz.id)

    def test_api_lists_quizzes(self):
        response = self.client.get(reverse('quizzes'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class AssignmentApiTestCase(SetupSchoolClassDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.student = Student.objects.create(name='Jhon Doe')
        cls.quiz = factories.create_quiz({ 'school_class': cls.school_class, 'questions': create_questions(2) })
        cls.enrollment = StudentEnrollment.objects.create(student=cls.student, school_class=cls.school_class)

    def test_api_creates_assignment(self):
        data = {
            'quiz': self.quiz.id,
            'enrollment': self.enrollment.id
        }
        url = reverse('student-assignments', kwargs={'student_id': self.student.id})

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 1)