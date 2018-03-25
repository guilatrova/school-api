from .models import Assignment, Submission, Quiz
from django.db.models import F

class GradeService:
    def check(self, assignment):
        status = self._get_status(assignment)
        grade = self._calc_grade(assignment) if status == Assignment.COMPLETED else 0

        assignment.status = status
        assignment.grade = grade
        assignment.save()
        
    def _get_status(self, assignment):
        submissions_made = Submission.objects.filter(assignment=assignment).count()

        if submissions_made > 0:
            if submissions_made == assignment.quiz.questions.count():
                return Assignment.COMPLETED
            else:
                return Assignment.IN_PROGRESS

        return Assignment.PENDING

    def _calc_grade(self, assignment):
        return Submission.objects.filter(
            assignment=assignment, 
            question__correct_answer=F('answer')
        ).count()