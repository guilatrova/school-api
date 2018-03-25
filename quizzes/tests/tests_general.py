from django.test import TestCase
from quizzes import views, serializers, factories, services
from quizzes.models import Quiz, Question, Answer, Assignment, Submission
from people.models import Teacher, Student
from classes.models import SchoolClass, StudentEnrollment
from common.tests.mixins import UrlTestMixin, UrlListTestMixin, BaseUrlTest
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

class ReportUrlsTestCase(BaseUrlTest, TestCase):
    def test_resolves_list_url(self):
        resolver = self.resolve_by_name('student-grades-report')
        self.assertEqual(resolver.func.cls, views.get_grade_report.cls)

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
        self.assert_grade(0)

    def test_service_calculates_grade(self):
        questions = self.quiz.questions.all()
        for question in questions[:2]:
            Submission.objects.create(assignment=self.assignment, question=question, answer=question.correct_answer)
        for question in questions[2:]:
            invalid_answer = question.correct_answer-1
            Submission.objects.create(assignment=self.assignment, question=question, answer=invalid_answer)

        self.service.check(self.assignment)
        self.assert_grade(2)

    def assert_status(self, status):
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, status)

    def assert_grade(self, grade):
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.grade, grade)

class GradeFactoryServiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = Teacher.objects.create(name='Kwan Lee')
        SchoolClass.objects.create(name='Managing great companies', teacher=cls.teacher)
        SchoolClass.objects.create(name='How to achieve greatness', teacher=cls.teacher)


    def test_service_generates_report_groupped_by_teacher_classes(self):
        factory = factories.GradeByClassReport(self.teacher.id)
        report = factory.generate()
        
        self.assertEqual(len(report), 2)
        self.assertIn('Managing great companies', report)
        self.assertIn('How to achieve greatness', report)


