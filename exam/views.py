from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Exam
from django.contrib import messages
import csv
# Create your views here.

def view_exams(request):
    if request.method == 'GET':
        exams = Exam.objects.all()
        return render(request, 'teacher_exam.html', {'exams':exams})
    else:
        pass

def delete_exam(request, exam_id = 0):
    Exam.objects.filter(id = exam_id).delete()
    messages.info(request, 'Exam record deleted!')
    return redirect('exams')

def view_exam(request, exam_id = 0):
    exam = Exam.objects.filter(id = exam_id)
    context=[]
    with open('auto-grade.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            context.append(row) 
    del context[0]
    return render(request, 'teacher_exam_view.html', {'exam':exam,'results':context})