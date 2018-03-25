from .models import Assignment, Submission, Quiz

class GradeService:
    def check(self, assignment):
        status = Assignment.PENDING
        submissions_made = Submission.objects.filter(assignment=assignment).count()

        if submissions_made > 0:
            status = Assignment.IN_PROGRESS

            if submissions_made == assignment.quiz.questions.count():
                status = Assignment.COMPLETED

        assignment.status = status
        assignment.save()    
