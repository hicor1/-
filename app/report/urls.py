# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('report_div_list/', views.report_div_list, name='report_div_list'),
    path('report_main/<int:Year>/<int:WeekNum>/<int:div_list_id>/<str:div1>/<str:div2>/', views.report_main, name='report_main'),
    ]