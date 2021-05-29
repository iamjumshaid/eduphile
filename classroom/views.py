from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Classroom
from .models import Student
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def classrooms(request):
    if request.method == 'POST':
        cls_id = request.POST['cls_id']
        std_email = request.POST['std_email']
        student = User.objects.filter(email = std_email)
        std = Student()
        std.class_id = cls_id
        std.student_id = student[0].id
        std.save()
        messages.info(request, 'Student added to classroom!')
        return redirect('classrooms')
    else:    
        who_is = request.user.is_staff
        if who_is: 
            classes = Classroom.objects.filter(teacher_id = request.user.id)
            return render(request, 'teacher_classroom.html', {'cls': classes})
        else:
            if request.session.has_key('is_logged'):
                del request.session['is_logged'] 
            return HttpResponse("Student interfaces coming soon.")

def create_classroom(request):
   clss = Classroom()
   clss.teacher_id = request.POST['teacher_id']
   clss.cls_name = request.POST['cls_name']
   clss.cls_desc = request.POST['cls_desc']
   clss.save()
   messages.info(request, 'Class has been created!.')
   return redirect('classrooms')

def open_classroom(request, cls_id = 0):
    my_class = Classroom.objects.filter(teacher_id = request.user.id, id = cls_id)
    std_ids = Student.objects.filter(class_id = cls_id)
    students = []
    for student_id in std_ids:
        students.append(student_id.student_id)
    stds = User.objects.in_bulk(students)
    return render(request, 'teacher_classroom_visit.html', {'myclass': my_class, 'studs' : stds})

def delete_classroom(request, cls_id = 0):
    Classroom.objects.filter(id = cls_id).delete()
    messages.info(request, 'Classroom deleted!')
    return redirect('classrooms')

def del_student(request, std_id = 0, cls_id = 0):
    Student.objects.filter(student_id = std_id).delete()
    url = '/teacher/open/classroom/{}/'.format(cls_id)
    messages.info(request, 'Student removed from classroom!')
    return redirect(url)

