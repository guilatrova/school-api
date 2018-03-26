from django.apps import AppConfig

class QuizzesConfig(AppConfig):
    name = 'quizzes'

    def ready(self):
        from quizzes import signals