from django.db import models

class HasAnswerChoices:
    ANSWER_CHOICES = (
        ('A', 1),
        ('B', 2),
        ('C', 3),
        ('D', 4),
    )

class Question(models.Model, HasAnswerChoices):
    description = models.CharField(max_length=100)
    correct_answer = models.PositiveSmallIntegerField(choices=HasAnswerChoices.ANSWER_CHOICES)

class Answer(models.Model, HasAnswerChoices):
    description = models.CharField(max_length=40)
    choice = models.PositiveSmallIntegerField(choices=HasAnswerChoices.ANSWER_CHOICES)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')