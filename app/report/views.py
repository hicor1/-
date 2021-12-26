#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.settings import LOGIN_REDIRECT_URL

from app.Utils.DB.DBQuery import Get_user_info

# Create your views here.

@login_required(login_url=LOGIN_REDIRECT_URL)
def report_main(request, Year, WeekNum, div_list_id, div1, div2):
    templates = 'report/report_main.html'

    #1. 페이지 호출
    if request.method=='GET':
    
        context = {
            'Year'       : Year,
            'WeekNum'    : WeekNum,
            'div_list_id': div_list_id,
            'div1'       : div1,
            'div2'       : div2
                   }
        return render(request, templates, context)

@login_required(login_url=LOGIN_REDIRECT_URL)
def report_div_list(request):
    templates = 'report/report_div_list.html'
    
    # User 사번으로부터 부서정보 받아오기
    사번 = request.user.first_name
    div1 = Get_user_info(사번=사번)['부서1'][0]

    
    if request.method=='GET':
        context = {'div1':div1,
                   }
        return render(request, templates, context)