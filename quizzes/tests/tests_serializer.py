from django.test import TestCase
from unittest.mock import patch, MagicMock
from quizzes import serializers, factories
from quizzes.models import Quiz, Question, Answer, Assignment, Submission
from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from .helpers import (
    SetupSchoolClassDataMixin, 
    SetupAssignmentDataMixin,
    SetupStudentEnrollmentDataMixin,
    SetupQuizDataMixin,
    create_questions, 
    create_question, 
    create_answers
)

class AnswerSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        data = { 'choice': 1, 'description': 'answer' }
        serializer = serializers.AnswerSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

class QuestionSerializerTestCase(TestCase):
    def test_serializer_validates(self):
        answers_data = create_answers('django', 'flask', 'cherry', 'none')
        question_data =  question_data =  create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_answer_validates_should_have_4_answers_choices(self):
        answers_data = create_answers('just', 'three', 'answers')
        question_data =  create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def test_answer_validates_should_not_allows_repetead_choices(self):
        answers_data = create_answers('yes', 'no', 'well...', 'I dont know')
        answers_data[1]['choice'] = 'A' #now we got two A choices
        question_data = create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def test_answer_validates_should_not_allows_repeated_answers(self):
        answers_data = create_answers('same', 'same', 'other', 'one more')
        question_data = create_question(answers_data)

        serializer = serializers.QuestionSerializer(data=question_data)
        self.assert_has_error(serializer, 'answers')

    def assert_has_error(self, serializer, key):
        self.assertFalse(serializer.is_valid())
        self.assertIn(key, serializer.errors)

class QuizSerializerTestCase(SetupSchoolClassDataMixin, TestCase):
    def test_serializer_validates(self):
        answers_data = create_answers('A', 'B', 'C', 'D')
        questions_data = [create_question(answers_data) for x in range(3)]
        data = { 'school_class': self.school_class.id, 'questions': questions_data }

        serializer = serializers.QuizSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    @patch('quizzes.factories.create_quiz', return_value=MagicMock())
    def test_serializer_creates(self, mock):
        answers_data = create_answers('A', 'B', 'C', 'D')
        questions_data = [create_question(answers_data) for x in range(3)]
        data = { 'school_class': self.school_class.id, 'questions': questions_data }

        serializer = serializers.QuizSerializer(data=data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()

        self.assertTrue(mock.called)
        self.assert_called_with_one_arg(mock)

    def assert_called_with_one_arg(self, mock):
        first_call = mock.call_args_list[0]
        args, kwargs = first_call
        self.assertEqual(len(args), 1)

class AssignmentSerializerTestCase(SetupStudentEnrollmentDataMixin, SetupQuizDataMixin, TestCase):
    def test_serializer_validates(self):
        data = { 'quiz': self.quiz.id, 'enrollment': self.enrollment.id }
        serializer = serializers.AssignmentSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_serializer_returns_status_and_grade(self):
        serializer = serializers.AssignmentSerializer(MagicMock())
        data = serializer.data
        self.assertIn('grade', data)
        self.assertIn('status', data)

class SubmissionSerializerTestCase(SetupAssignmentDataMixin, TestCase):
    def setUp(self):
        self.context = { 'assignment_id': self.assignment.id }

    def test_serializer_validates(self):
        data = { 'question': self.quiz.questions.first().id, 'answer': 1 }
        serializer = serializers.SubmissionSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_serializer_question_validate_should_not_allows_duplicates(self):
        question = self.quiz.questions.first()
        Submission.objects.create(assignment=self.assignment, question=question, answer=1)
        data = { 'question': self.quiz.questions.first().id, 'answer': 1 }

        serializer = serializers.SubmissionSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('question', serializer.errors)

    def test_serializer_question_validate_should_belong_to_assigned_quiz(self):
        other_quiz = factories.create_quiz({ 'school_class': self.school_class, 'questions': create_questions(1) })
        data = { 'question': other_quiz.questions.first().id, 'answer': 1 }

        serializer = serializers.SubmissionSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('question', serializer.errors)