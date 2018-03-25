from django.db import models

class HasAnswerChoices:
    ANSWER_CHOICES = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    )

class Submission(models.Model, HasAnswerChoices):
    """
    Represents an answer for an assignment's question provided by user
    """
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.PositiveSmallIntegerField(choices=HasAnswerChoices.ANSWER_CHOICES)

class Assignment(models.Model):
    PENDING = 'P'
    IN_PROGRESS = 'IP'
    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (IN_PROGRESS, 'IN PROGRESS')
    )

    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    enrollment = models.ForeignKey('classes.StudentEnrollment', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)

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