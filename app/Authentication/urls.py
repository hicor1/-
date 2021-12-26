# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'Authentication'

urlpatterns = [
    path('Login',  views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),
    path('Register', views.Register, name='Register'),
    ]