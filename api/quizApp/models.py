from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver 

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

class Student(models.Model):
    index = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'student - {self.index} named {self.first_name} {self.last_name}'
    
    # def get_assesment(self):
    #     submissions =


class Submission(models.Model):
    student = models.ForeignKey(Student, related_name="submission", on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=True)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.index} submitted {self.selected_option} for {self.question} in {self.quiz}"


class Assessment(models.Model):
    student = models.ForeignKey(Student, related_name="Assessment", on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, related_name="Assessment", on_delete=models.CASCADE, null=True, blank=True)
    score = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.student.first_name} {self.student.last_name} Assessments'
    


@receiver(post_save, sender=Submission)
def record_assessment(sender, instance, created, **kwargs):
    # print(instance,created)
    if not instance.submitted:
        # get existing assement record or create new one 
        assessment, created = Assessment.objects.get_or_create(student=instance.student,quiz=instance.quiz)
        submissions = Submission.objects.filter(student=instance.student, quiz=instance.quiz)

        # this loops gets all subitted answers under the said questions and calculates their total
        total_score = 0
        for submission in submissions:
            if submission.selected_option.is_correct:
                total_score += 1
        assessment.score = total_score
        assessment.save()

        # ensuring a submitted answer does not get counted twice
        instance.submitted = True 
        instance.save()

            
        