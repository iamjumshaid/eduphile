from django.contrib import admin
from . models import Classroom
from . models import Student
# Register your models here.
admin.site.register(Classroom)
admin.site.register(Student)