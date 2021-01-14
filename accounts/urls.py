from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page, name = 'home'),
    path('signup', views.register_page, name = 'register')
]