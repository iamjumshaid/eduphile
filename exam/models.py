from django.db import models

# Create your models here.

class Exam(models.Model):
    cls_name = models.TextField()
    total_std = models.IntegerField()
    total_attempts = models.IntegerField()
    exam_created = models.DateTimeField(auto_now_add=True)    

class Exam_Details(models.Model):
    exam_name = models.TextField()
    class_id = models.SmallIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Questions(models.Model):
    exam_id = models.SmallIntegerField()
    question = models.TextField()
    correct_ans = models.TextField()
    question_marks = models.SmallIntegerField()
    question_type = models.TextField()
    std_id = models.SmallIntegerField(null=True)
    std_answer = models.TextField(null=True)

class Mcqs(models.Model):
    question_id = models.SmallIntegerField()
    option = models.TextField()