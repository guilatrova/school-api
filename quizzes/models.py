from django.db import models

class Question(models.Model):
    ANSWER_CHOICES = (
        ('A', 1),
        ('B', 2),
        ('C', 3),
        ('D', 4),
    )

    description = models.CharField(max_length=100)
    correct_answer = models.PositiveSmallIntegerField(choices=ANSWER_CHOICES)

class Answer(models.Model):
    ANSWER_CHOICES = (
        ('A', 1),
        ('B', 2),
        ('C', 3),
        ('D', 4),
    )

    description = models.CharField(max_length=40)
    choice = models.PositiveSmallIntegerField(choices=ANSWER_CHOICES)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')