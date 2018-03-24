from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('people.Teacher', on_delete=models.PROTECT)