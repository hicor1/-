#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render

from rest_framework.response import Response

from app.Utils.DB.DBQuery                 import AuthRegist, DBSpecificQuery
from app.Utils.Report.CreateReportTable   import CallReportTemplate
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

class RegistViewset(ModelViewSet):

    @action(detail=False, methods=['POST'])
    #@csrf_protect
    def GetDivList(self, request):
        col     = self.request.data["col"] # 1 or 2
        div1    = self.request.data["div1"]
        div2    = self.request.data["div2"]

        #. 본부 검색의 경우, 필터링 없이 전부 보여준다
        if col=="1":
            collist = ["div1"]
            div1    = ""
            div2    = ""
        #. 센터 검색의 경우, 해당본부에 해당하는 센터만 보여준다.
        elif col=="2":
            collist = ["div1","div2"]
            div1    = div1
            div2    = div2

        if True:
            
            df_Raw = DBSpecificQuery(
                ConnectInfo, 
                TableName    = 'div_list', 
                ColumnList   = collist, # "*" 도 가능
                QueryDict    = {"div1":div1, "div2":div2},
                SortField    = "div1",
                Sortby       = "ASC",
                Limit        = "30" 
                )
            # Json타입 변경
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
