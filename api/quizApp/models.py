from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    name = models.CharField(max_length=255)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_all_quizes(self):
        quizes = self.quiz.all()
        return quizes 

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    classroom = models.ForeignKey(Classroom, related_name="quiz", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_all_questions(self):
        questions = self.question.all()
        return questions


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="question", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
    def get_all_options(self):
        options = self.option.all()
        return options



class Option(models.Model):
    question = models.ForeignKey(Question, related_name="option", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
