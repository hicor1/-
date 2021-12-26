#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from rest_framework.response import Response

from app.Utils.DB.DBQuery                 import AuthRegist
from app.Utils.Report.CreateReportTable   import CallReportTemplate, ReportRegist, GetReportDetail, ReportDelete, ReportModify
from app.Utils.Report.CreateDivList       import CreateDivHTML

from app.settings  import DATABASES

from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json, re

# DB direct 연결정보
ConnectInfo = {
    'host'     :DATABASES["default"]["HOST"],
    'dbname'   :DATABASES["default"]["NAME"],
    'user'     :DATABASES["default"]["USER"],
    'password' :DATABASES["default"]["PASSWORD"],
    'port'     :DATABASES["default"]["PORT"], #4040, 5432
    'options'  :'-c search_path=dbo,public'
    }

#@login_required
#@authentication_classes((JSONWebTokenAuthentication,)) #. JWT토큰검사 ( setting에서 JWT옵션 포함해줘야함 )

class ReportViewset(ModelViewSet):

    @action(detail=False, methods=['GET'])
    #@csrf_protect
    #. 본부~센터 리스트 얻기
    def GetDivList(self, request):

        div1 = self.request.GET["div1"]
        div2 = self.request.GET["div2"]

        df_Raw = CreateDivHTML(div1, div2) # Blank일 경우, 전체 반환 / 특정 부서 지정가능
        # Json타입 변경
        processtime  = df_Raw['processtime(ms)']
        df_Raw       = df_Raw['df']

        return Response({
            "processtime(ms)"  :processtime, # ????????? ????
            "Count"            :len(df_Raw), # ????????? ????
            "data"             :df_Raw, # ?????????
            })


    @action(detail=False, methods=['GET'])
    #@csrf_protect
    #. 주간업무보고 리스트 얻기
    def ReportView(self, request):

        div_list_id = self.request.GET["div_list_id"]
        Year        = self.request.GET["Year"]
        WeekNum     = self.request.GET["WeekNum"]

        #. (ID_get) Session정보를 바탕으로 request요청한 사용자 ID 받아오기(참고)https://stackoverflow.com/questions/235950/how-to-lookup-django-session-for-a-particular-user
        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        UserID = session.get_decoded().get('_auth_user_id') #user = User.objects.get(pk=uid)


        if div_list_id:
            
            df_Raw = CallReportTemplate(div_list_id, Year, WeekNum, UserID)
            # Json타입 변경
            processtime  = df_Raw['processtime(ms)']
            #.(21.07.06추가) 보고서 등록사람 df에 저장
            RegisterdedPerson = df_Raw['RegisterdedPerson']
            df_Raw       = df_Raw['df']

            return Response({
                "processtime(ms)"   :processtime, # ????????? ????
                "Count"             :len(df_Raw), # ????????? ????
                "data"              :df_Raw, # ?????????
                "RegisterdedPerson" : RegisterdedPerson
                })

        else: # if tech_code in Request from client, return blank data
            return Response({
                "processtime(ms)"  :"", # ????????? ????
                "Count"            :0, 
                "data"             :[], 
                })

    #. 주간업무보고 보고내용 등록
    @action(detail=False, methods=['POST'])
    def ReportRegist(self, request):

        #. Form submit으로 넘어온 데이터
        data = self.request.data
        #. csrf를 제외한, form데이터만 추출
        data = data["formdata"]
        #. String타입 데이터를 dict(json)으로 변경
        data = json.loads(data)

        if data:
            #. DB에 저장 ㄱㄱ
            df_Raw = ReportRegist(data = data)

            processtime  = df_Raw['processtime(ms)']
            df_Raw       = df_Raw['Msg']
            
            return Response({
                "processtime(ms)"  :processtime, # ????????? ????
                "Count"            :1, # ????????? ????
                "data"             :df_Raw, # ?????????
                })

        else: # if tech_code in Request from client, return blank data
            return Response({
                "processtime(ms)"  :"", # ????????? ????
                "Count"            :0, 
                "data"             :[], 
                })

    #. 주간업무보고 Detail 사항 보여주기
    @action(detail=False, methods=['POST'])
    def GetReportDetail(self, request):

        #. Form submit으로 넘어온 데이터
        data = self.request.data
        #. csrf를 제외한, ReportID데이터만 추출
        ReportID = data["ReportID"]

        if ReportID:
            #. 주간업무보고 Detail 가져오기
            df_Raw = GetReportDetail(ReportID)
            processtime  = df_Raw['processtime(ms)']
            df_Raw       = df_Raw['df'].to_dict(orient='records')

            return Response({
                "processtime(ms)"  :processtime, # ????????? ????
                "Count"            :len(df_Raw), # ????????? ????
                "data"             :df_Raw, # ?????????
                })

        else: # if tech_code in Request from client, return blank data
            return Response({
                "processtime(ms)"  :"", # ????????? ????
                "Count"            :0, 
                "data"             :[], 
                })

    #. 주간업무보고 삭제하기
    @action(detail=False, methods=['POST'])
    def ReportDelete(self, request):

        #. Form submit으로 넘어온 데이터
        data = self.request.data
        #. csrf를 제외한, ReportID데이터만 추출
        ReportID = data["ReportID"]

        if ReportID:
            #. 주간업무보고 Detail 가져오기
            df_Raw = ReportDelete(ReportID)
            processtime  = df_Raw['processtime(ms)']
            df_Raw       = df_Raw['df'].to_dict(orient='records')

            return Response({
                "processtime(ms)"  :processtime, # ????????? ????
                "Count"            :len(df_Raw), # ????????? ????
                "data"             :df_Raw, # ?????????
                })

        else: # if tech_code in Request from client, return blank data
            return Response({
                "processtime(ms)"  :"", # ????????? ????
                "Count"            :0, 
                "data"             :[], 
                })


    #. 주간업무보고 보고내용 수정
    @action(detail=False, methods=['POST'])
    def ReportModify(self, request):

        #. Form submit으로 넘어온 데이터
        data = self.request.data
        #. csrf를 제외한, form데이터만 추출
        data = data["formdata"]
        #. String타입 데이터를 dict(json)으로 변경
        data = json.loads(data)

        #. RequestID와 수정할 보고의 ID를 비교하여 일치하는지 확인 ㄱㄱ
        #(1). UserID
        session_key = request.session.session_key
        session = Session.objects.get(session_key=session_key)
        UserID = session.get_decoded().get('_auth_user_id') #user = User.objects.get(pk=uid)
        #(2). 수정할 보고의 ID
        작성자ID = data["작성자ID"]

        #. 요청자 및 요청글 작성자가 서로 일치하는 경우에만 수정 허용
        if UserID == 작성자ID:
            #. DB에 저장 ㄱㄱ
            df_Raw = ReportModify(data = data)

            processtime  = df_Raw['processtime(ms)']
            df_Raw       = df_Raw['df']
            
            return Response({
                "processtime(ms)"  :processtime, # ????????? ????
                "Count"            :1, # ????????? ????
                "data"             :df_Raw, # ?????????
                })

        else: # if tech_code in Request from client, return blank data
            return Response({
                "processtime(ms)"  :"", # ????????? ????
                "Count"            :0, 
                "data"             :[], 
                })