from django.test import TestCase
from quizzes import views, serializers, factories, services
from quizzes.models import Quiz, Question, Answer, Assignment, Submission
from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from common.tests.mixins import UrlTestMixin, UrlListTestMixin
from .helpers import SetupSchoolClassDataMixin, SetupAssignmentDataMixin, create_questions, create_question, create_answers

class QuizUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'quizzes'
    single_name = 'quiz'
    allowed_single = ['get']
    view = views.QuizViewSet

class AssignmentUrlsTestCase(UrlTestMixin, TestCase):
    list_name = 'assignments'
    single_name = 'assignment'
    allowed_single = ['get']
    allowed_list = ['get']
    view = views.AssignmentViewSet

class SubmissionUrlsTestCase(UrlListTestMixin, TestCase):
    list_name = 'assignment-submissions'
    list_params = {'assignment_id': 1}
    allowed_list = ['get', 'post']
    view = views.SubmissionViewSet

class FactoriesTestCase(SetupSchoolClassDataMixin, TestCase):
    def setUp(self):
        answers = create_answers('A', 'B', 'C', 'D')
        questions = [create_question(answers) for x in range(3)]
        self.data = {
            'school_class': self.school_class,
            'questions': questions
        }

    def test_create_quiz(self):
        factories.create_quiz(self.data)

        self.assertEqual(Answer.objects.count(), 4 * 3)
        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Quiz.objects.count(), 1)

class GradeServiceTestCase(SetupAssignmentDataMixin, TestCase):
    def setUp(self):
        self.service = services.GradeService()

    def test_service_without_any_submission_remains_pending(self):
        self.service.check(self.assignment)
        self.assert_status(Assignment.PENDING)

    def test_service_updates_to_in_progress_when_any_submissions_is_made(self):
        Submission.objects.create(assignment=self.assignment, question=self.quiz.questions.first(), answer=1)
        self.service.check(self.assignment)
        self.assert_status(Assignment.IN_PROGRESS)    

    def test_service_updates_to_completed_when_all_submissions_are_made(self):
        for question in self.quiz.questions.all():
            Submission.objects.create(assignment=self.assignment, question=question, answer=1)

        self.service.check(self.assignment)
        self.assert_status(Assignment.COMPLETED)

    def test_service_only_calculates_grade_when_completed(self):        
        question = self.quiz.questions.first()
        Submission.objects.create(assignment=self.assignment, question=question, answer=question.correct_answer)
        self.service.check(self.assignment)
        self.assertEqual(self.assignment.grade, 0)

    def assert_status(self, status):
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, status)
        
    #TODO calculates grade
    #TODO cant submit same question twice