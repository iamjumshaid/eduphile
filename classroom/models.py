from django.db import models

# Create your models here.

class Classroom(models.Model):
    teacher_id = models.IntegerField()
    cls_name = models.CharField(max_length=100)
    cls_desc = models.TextField()

class Student(models.Model):
    class_id = models.IntegerField()
    student_id = models.IntegerField()

