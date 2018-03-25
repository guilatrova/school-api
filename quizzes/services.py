from .models import Assignment, Submission, Quiz
from django.db.models import F

class GradeService:
    def check(self, assignment):
        status = Assignment.PENDING
        grade = 0
        submissions_made = Submission.objects.filter(assignment=assignment).count()

        if submissions_made > 0:
            status = Assignment.IN_PROGRESS

            if submissions_made == assignment.quiz.questions.count():
                status = Assignment.COMPLETED
                grade = Submission.objects.filter(assignment=assignment, question__correct_answer=F('answer')).count()

        assignment.status = status
        assignment.grade = grade
        assignment.save()    
