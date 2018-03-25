from .models import Assignment, Submission

class GradeService:
    def check(self, assignment_id):
        status = Assignment.PENDING
        if Submission.objects.filter(assignment_id=assignment_id).exists():
            status = Assignment.IN_PROGRESS

        assignment = Assignment.objects.get(pk=assignment_id)
        assignment.status = status
        assignment.save()
