from django.db import models

class HasAnswerChoices:
    ANSWER_CHOICES = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    )

class Assignment(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    enrollment = models.ForeignKey('classes.StudentEnrollment', on_delete=models.CASCADE)

class Quiz(models.Model):
    school_class = models.ForeignKey('classes.SchoolClass', on_delete=models.PROTECT)    

class Question(models.Model, HasAnswerChoices):
    description = models.CharField(max_length=100)
    correct_answer = models.PositiveSmallIntegerField(choices=HasAnswerChoices.ANSWER_CHOICES)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')

class Answer(models.Model, HasAnswerChoices):
    description = models.CharField(max_length=40)
    choice = models.PositiveSmallIntegerField(choices=HasAnswerChoices.ANSWER_CHOICES)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')