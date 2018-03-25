from .models import Assignment, Submission

class GradeService:
    def check(self, assignment_id):
        status = Assignment.PENDING
        if Submission.objects.filter(assignment_id=assignment_id).exists():
            status = Assignment.IN_PROGRESS

        Assignment.objects\
            .filter(pk=assignment_id)\
            .update(status=status)
