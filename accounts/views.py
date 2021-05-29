from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .models import Profile
from django.core.files.storage import FileSystemStorage
# Create your views here.

def login_page(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = auth.authenticate(username = username, password = password)
       if user is not None:
           auth.login(request, user)
           request.session['is_logged'] = True
           return redirect('classrooms')
       else:
           messages.info(request, 'invalid credentials!')
           return render(request, 'login.html')
    else:
        if request.session.has_key('is_logged'):
            return redirect("classrooms")
        else:
            return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        if User.objects.filter(email = request.POST['email']).exists():
            messages.info(request, 'User email already exists!')
            return render(request, 'signup.html')
        elif User.objects.filter(username = request.POST['username']).exists():
            messages.info(request, 'Username already exists!')
            return render(request, 'signup.html')
        else:
            user_name = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            f_name = request.POST['fname']
            l_name = request.POST['lname']
            if request.POST['staff'] == 'teacher':
                is_staff = True 
            else:
                is_staff = False
            user = User.objects.create_user(
                username = user_name,
                password = password,
                email = email,
                is_staff = is_staff,
                first_name = f_name,
                last_name = l_name
                )
            user.save()
            messages.info(request, 'Account created! Login to continue.')
            return redirect('home')
    else:
        if request.session.has_key('is_logged'):
            return redirect('classrooms')
        else:
            return render(request, 'signup.html')

def logout(request):
    if request.session.has_key('is_logged'):
        del request.session['is_logged'] 
    return redirect('home')

def edit(request):
    if request.method == 'POST':
        user = User.objects.get(username = request.POST['uname'])
        print(user)
        if user.check_password(request.POST['currentPass']):
           user.first_name = request.POST['fname']
           user.last_name = request.POST['lname']
           user.set_password(request.POST['newPass'])
           #image_name = request.POST['profPic'].replace(' ', '_')
           #user.profile.img = 'pics/' + image_name
           myfile = request.FILES['profPic']
           fs = FileSystemStorage()
           filename = fs.save(myfile.name, myfile)
           uploaded_file_url = fs.url(filename)
           user.profile.img = uploaded_file_url
           
           print(uploaded_file_url)
           user.save()
           user = auth.authenticate(username = request.POST['uname'], password = request.POST['newPass'])
           auth.login(request, user)
           request.session['is_logged'] = True
           messages.info(request, 'Your profile has been updated!')
           return redirect('edit/profile')
        else:
           messages.info(request, 'Current credentials do not match!')
           return redirect('edit/profile')
    else:
        if request.session.has_key('is_logged'):
            return render(request, 'edit-user-profile.html')
        else:
            return render(request, 'login.html')

