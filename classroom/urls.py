from django.urls import path
from . import views

urlpatterns = [
    path('classrooms', views.classrooms, name = 'classrooms'),
    path('create/classroom', views.create_classroom, name = 'create/classroom')
]