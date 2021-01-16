from django.urls import path
from . import views

urlpatterns = [
    path('exams', views.view_exams, name = 'exams'),
    path('exams/del/<int:exam_id>/', views.delete_exam),
    path('exams/view/<int:exam_id>/', views.view_exam),
  ]