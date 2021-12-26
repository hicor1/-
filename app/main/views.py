#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.settings import LOGIN_REDIRECT_URL

# Create your views here.

@login_required(login_url=LOGIN_REDIRECT_URL)
def main(request):
    templates = 'main/main.html'
    if request.method=='GET':
        context = {'':'',
                   }
        return render(request, templates, context)

