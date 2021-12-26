#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#. 로그인 관련 모듈
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse

from app.Utils.DB.DBQuery import AuthRegist, Auth_Duplicate_check

from app.settings import LOGIN_REDIRECT_URL

# Create your views here.
#(참고)https://wayhome25.github.io/django/2017/03/01/django-99-my-first-project-2/
#(참고)https://han-py.tistory.com/148

#@login_required
def Login(request):
    templates = 'Authentication/Login.html'
    
    #. 로그인 요청 (Form Submit)
    if request.method=='POST':
        사번 = request.POST['사번']
        비밀번호 = request.POST['비밀번호']

        #. 로그인은 반드시 이름(username)으로 해야하므로, 사번에 맞는 이름 조회
        이름 = User.objects.get(first_name=사번).username
        #. 사번으로 조회한 이름과 비밀번호를 기준으로 로그인 시도
        user = auth.authenticate(username = 이름, password = 비밀번호)
        if user is not None:
            auth.login(request, user) # 세션에 로그인 데이터 기록 및 클라이언트 쿠키에 저장
            return redirect('/main')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')

    #. 로그인 페이지 호출
    elif request.method=='GET':
         #. 이미 로그인한 상태라면, 메인으로 돌려보내기
        if request.user.is_authenticated:
            return redirect('/main')

        context = {'':'',
                   }
        return render(request, templates, context)


@login_required(login_url=LOGIN_REDIRECT_URL)
def Logout(request):
    auth.logout(request)
    return redirect('/main')
    

def Register(request):
    templates = 'Authentication/Register.html'

    #. 회원가입 요청 (Form Submit)
    if request.method=='POST':

        username   = request.POST['이름']
        email      = request.POST['이메일']
        password1  = request.POST['비밀번호']
        password2  = request.POST['비밀번호확인']

        first_name = request.POST['사번']
        
        부서1 = request.POST['소속본부']
        부서2 = request.POST['소속센터']
        기타 = request.POST['비고(기타)']

        #. 존재하는 회원인지 확인
        Duplicate = Auth_Duplicate_check(사번 = first_name, username = username, email=email)

        if Duplicate == True: # 중복된 아이디가 있는 경우,
            return render(request, templates, {'warning':"[이름] 또는 [사번] 또는 [e-mail] 이 존재합니다."})
        elif password1 != password2: # 비밀번호가 일치하지 않는 경우,
            return render(request, templates, {'warning':"Password가 일치하지 않습니다."})
        else: # 아무 문제가 없는 경우
            #. 회원기본정보 입력
            user = User.objects.create_user(
                username   = username,
                first_name = first_name,
                email      = email,
                password   = password1,
            )
            #. 회원 추가정보 입력
            AuthRegist(
                사번   = first_name, 
                부서1  = 부서1, 
                부서2  = 부서2, 
                기타   = 기타
            )

            auth.login(request, user)
            return redirect('/main')

        return render(request, templates)
        
    #. 회원가입 페이지 호출
    elif request.method=='GET':
        #. 이미 로그인한 상태라면, 메인으로 돌려보내기
        if request.user.is_authenticated:
            return redirect('/main')

        context = {'':'',
                   }

        return render(request, templates, context)