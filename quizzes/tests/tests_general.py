from datetime import date
from unittest.mock import patch
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

class SignalsIntegrationTestCase(SetupAssignmentDataMixin, TestCase):
    @patch('quizzes.services.GradeService.check')
    def test_creating_a_submission_calls_grade_service(self, mock):
        question = self.quiz.questions.first()
        submission = Submission.objects.create(assignment=self.assignment, question=question, answer=1)

        mock.assert_called_with(self.assignment)

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
        #people
        cls.teacher = Teacher.objects.create(name='Kwan Lee')
        cls.student1 = Student.objects.create(name='Guilherme Latrova')
        cls.student2 = Student.objects.create(name='John Doe')
        #classes
        cls.class1 = SchoolClass.objects.create(name='Managing great companies', teacher=cls.teacher)
        cls.class2 = SchoolClass.objects.create(name='How to achieve greatness', teacher=cls.teacher)
        #enrollment
        student1_management = StudentEnrollment.objects.create(student=cls.student1, school_class=cls.class1, semester=date(2018, 1, 1))
        student2_management = StudentEnrollment.objects.create(student=cls.student2, school_class=cls.class1, semester=date(2018, 1, 1))
        student1_greatness = StudentEnrollment.objects.create(student=cls.student1, school_class=cls.class2,  semester=date(2018, 1, 1))
        student1_greatness2 = StudentEnrollment.objects.create(student=cls.student1, school_class=cls.class2, semester=date(2018, 7, 1))
        #quizzes
        quiz1 = factories.create_quiz({ 'school_class': cls.class1, 'questions': create_questions(5) })
        quiz2 = factories.create_quiz({ 'school_class': cls.class1, 'questions': create_questions(5) })
        quiz3 = factories.create_quiz({ 'school_class': cls.class2, 'questions': create_questions(10)})
        quiz4 = factories.create_quiz({ 'school_class': cls.class2, 'questions': create_questions(10) })
        #assignments
        Assignment.objects.create(quiz=quiz1, enrollment=student1_management, status=Assignment.COMPLETED, grade=4)
        Assignment.objects.create(quiz=quiz2, enrollment=student1_management, status=Assignment.COMPLETED, grade=5)
        Assignment.objects.create(quiz=quiz1, enrollment=student2_management, status=Assignment.COMPLETED, grade=3)
        Assignment.objects.create(quiz=quiz2, enrollment=student2_management, status=Assignment.COMPLETED, grade=3)
        Assignment.objects.create(quiz=quiz3, enrollment=student1_greatness, status=Assignment.COMPLETED, grade=9)
        Assignment.objects.create(quiz=quiz4, enrollment=student1_greatness2, status=Assignment.COMPLETED, grade=10) #Not returned

    def setUp(self):
        factory = factories.GradeByClassReport(self.teacher.id, date(2018, 1, 1))
        self.report = factory.generate()

    def test_generates_report_grouped_by_teacher_classes(self):                
        self.assertEqual(len(self.report), 2)
        self.assertIn('Managing great companies', self.report)
        self.assertIn('How to achieve greatness', self.report)

    def test_generates_report_with_enrolled_students_inside_classes(self):        
        self.assertEqual(len(self.report[self.class1.name]), 2)
        self.assertEqual(len(self.report[self.class2.name]), 1)
        self.assertIn(self.student1.name, self.report[self.class1.name])
        self.assertIn(self.student1.name, self.report[self.class2.name])
        self.assertIn(self.student2.name, self.report[self.class1.name])

    def test_generates_report_with_sum_grade_inside_students(self):
        class1 = self.report[self.class1.name]
        class2 = self.report[self.class2.name]

        self.assertEqual(class1[self.student1.name], 9)
        self.assertEqual(class1[self.student2.name], 6)
        self.assertEqual(class2[self.student1.name], 9)