from django.db import models

class Answer(models.Model):
    ANSWER_CHOICES = (
        ('A', 1),
        ('B', 2),
        ('C', 3),
        ('D', 4),
    )

    description = models.CharField(max_length=40)
    choice = models.PositiveSmallIntegerField(choices=ANSWER_CHOICES)
