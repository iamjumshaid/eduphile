from datetime import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Classroom
from .models import Student
from exam.models import Exam_Details
from exam.models import Questions
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
            # preparing data for student classes interface
            class_ids = Student.objects.filter(student_id = request.user.id).values_list('class_id', flat=True)
            std_classes = Classroom.objects.filter(id__in= class_ids)
            #print(std_classes)
            '''
            for c_id in class_ids:
                print(type(c_id), c_id)
            for c in std_classes:
                print(c.id, c.cls_name, c.cls_desc)
            #return HttpResponse(class_ids)
            '''
            return render(request, 'student_classroom.html', {'std_classes': std_classes})

def create_classroom(request):
   clss = Classroom()
   clss.teacher_id = request.POST['teacher_id']
   clss.cls_name = request.POST['cls_name']
   clss.cls_desc = request.POST['cls_desc']
   clss.save()
   messages.info(request, 'Class has been created!.')
   return redirect('classrooms')

def open_classroom(request, cls_id = 0):
    if request.user.is_staff:
        my_class = Classroom.objects.filter(teacher_id = request.user.id, id = cls_id)
        std_ids = Student.objects.filter(class_id = cls_id)
        students = []
        for student_id in std_ids:
            students.append(student_id.student_id)
        stds = User.objects.in_bulk(students)
        return render(request, 'teacher_classroom_visit.html', {'myclass': my_class, 'studs' : stds})
    else: 
        # preparing data for student classroom view
        class_details = Classroom.objects.filter(id = cls_id)
        class_name = ""
        teacher_name = ""
        exam_status = []
        is_attempted = []

        # teacher name and class name
        for cd in class_details:
            teacher_details = User.objects.filter(id = cd.teacher_id)
            class_name = cd.cls_name
        for td in teacher_details:
            f_name = td.first_name
            l_name = td.last_name
            teacher_name = f_name + ' ' + l_name

        print("printing:",class_name, teacher_name)

        # exam name, details and attempted or not
        exam_details = Exam_Details.objects.filter(class_id = cls_id)
        from django.utils import timezone
        date_time_now = timezone.now()
        for ed in exam_details:
            print(ed.exam_name, ed.start_time, ed.end_time)
            if date_time_now < ed.end_time:
                exam_status.append("Available")
            else:
                exam_status.append("Not Available")
            if Questions.objects.filter(std_id = request.user.id, exam_id = ed.id).exists():
                is_attempted.append(True)
            else:
                is_attempted.append(False)
            print(is_attempted)
        #return HttpResponse('student class and its exam details')
        return render(request, 'student_classroom_visit.html', {
            'exams': exam_details, 
            'class_name' : class_name,
            'teacher_name' : teacher_name,
            'exam_status' : exam_status,
            'is_attempted' : is_attempted
            })

def delete_classroom(request, cls_id = 0):
    if request.user.is_staff:
        Classroom.objects.filter(id = cls_id).delete()
        messages.info(request, 'Classroom deleted!')
        return redirect('classrooms')
    else:
        Student.objects.filter(class_id = cls_id).delete()
        messages.info(request, 'You left the classroom!')
        return redirect('classrooms')

def del_student(request, std_id = 0, cls_id = 0):
    Student.objects.filter(student_id = std_id).delete()
    url = '/teacher/open/classroom/{}/'.format(cls_id)
    messages.info(request, 'Student removed from classroom!')
    return redirect(url)

