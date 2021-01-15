from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Classroom
from django.contrib import messages
# Create your views here.

def classrooms(request):
    who_is = request.user.is_staff
    if who_is == True: 
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


        
