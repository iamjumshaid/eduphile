from django.db import models

# Create your models here.

class Exam(models.Model):
    cls_name = models.TextField()
    total_std = models.IntegerField()
    total_attempts = models.IntegerField()
    exam_created = models.DateTimeField(auto_now_add=True)    
