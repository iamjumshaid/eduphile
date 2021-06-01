from django.contrib import admin
from .models import Exam, Exam_Details, Mcqs, Questions
# Register your models here.
admin.site.register(Exam)
admin.site.register(Exam_Details)
admin.site.register(Questions)
admin.site.register(Mcqs)