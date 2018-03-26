from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submission
from .services import GradeService

@receiver(post_save, sender=Submission)
def check_grade(sender, instance=None, created=False, **kwargs):
    assignment = instance.assignment
    GradeService().check(assignment)