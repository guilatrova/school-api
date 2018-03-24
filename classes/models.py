from django.db import models
from people.models import Teacher

class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)