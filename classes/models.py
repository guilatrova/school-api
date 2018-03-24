from django.db import models

class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('people.Teacher', on_delete=models.PROTECT)

class StudentEnrollment(models.Model):
    student = models.ForeignKey('people.Student', on_delete=models.PROTECT)
    school_class = models.ForeignKey('SchoolClass', on_delete=models.PROTECT)