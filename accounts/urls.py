from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name = 'home'),
    path('signup', views.register_page, name = 'register'),
    path('logout', views.logout, name = 'logout')
]