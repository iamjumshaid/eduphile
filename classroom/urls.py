from django.urls import path
from . import views

urlpatterns = [
    path('classrooms', views.classrooms, name = 'classrooms'),
    path('create/classroom', views.create_classroom, name = 'create/classroom'),
    path('open/classroom/<int:cls_id>/', views.open_classroom),
    path('delete/classroom/<int:cls_id>/', views.delete_classroom),
    path('del/student/<int:std_id>/<int:cls_id>/', views.del_student, name = 'del_student')
]