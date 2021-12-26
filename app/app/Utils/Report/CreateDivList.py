# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 11:49:48 2021

@author: hicor
"""

#%%
import pandas as pd
import timeit
import os
import psycopg2
import datetime
#%% DB 연결정보
DB_CONN = {'host'     :os.environ.get("SQL_HOST",     "3.37.42.132"),
           'dbname'   :os.environ.get("SQL_DATABASE", "report"),
           'user'     :os.environ.get("SQL_USER",     "hicor"),
           'password' :os.environ.get("SQL_PASSWORD", "dlacodnr1!"),
           'port'     :os.environ.get("SQL_PORT",     "4040"),
           'options'  :'-c search_path=dbo,public'}

#%%HTML태그 만들기
#. BaseHtml 함수정의
def GetBaseHtml(div1, div2):
    BaseHtml='''
        <div class="col-12 ">
            <div class="card">
                <div class="card-header">
                    <h4 style="font-weight: 700;">{div1}</h4>
                </div>
                <div class="card-body">
                    <p class="text-muted">해당하는 센터 또는 부서를 선택하세요.</p>
                    <div class="buttons">
                    {div2}
                    </div>
                </div>
            </div>
        </div>
    '''.format(div1=div1, div2=div2)
    return BaseHtml
#%% 부서정보 받아와서 HTML로 변경 (전체부서)
def CreateDivHTML(div1, div2):
    #. 빈데이터 생성
    df_Raw={}
    
    ##. 구분자 확인
    #. 본부명이 있다면, 본부에 해당하는 리스트만 반환/ 본부명 없으면 전부다
    div1 = div1
    #. 센터멍이 있다면, 센터에 해당하는 class에 active 추가
    div2 = div2
    
    #. 시작시간 체크
    tic=timeit.default_timer()
    
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = DB_CONN['host'],
                            dbname   = DB_CONN['dbname'],
                            user     = DB_CONN['user'],
                            password = DB_CONN['password'],
                            port     = DB_CONN['port'],
                            options  = DB_CONN['options'])
    cur = conn.cursor()
    
    #. 쿼리변수 정의
    TableName = "div_list"
    SELECT   = "*" 
    LIMIT     = "999"
    
    #. 쿼리조합 ( concat은 문자열 합치기 ) # 유사한 경우도 포함하여 쿼리한다. 
    SQL = """
        SELECT     {SELECT}
        FROM       "{TableName}"
        WHERE      "div1" ilike '%{div1}%'
        ORDER BY   div1 DESC, div2 ASC
        LIMIT      {LIMIT}
        """.format(
        SELECT    = SELECT,
        TableName = TableName,
        div1      = div1,
        LIMIT     = LIMIT
        )
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        Result = pd.read_sql(SQL, conn)
    except:
        Result = pd.DataFrame() # 빈 데이터 프레임 리턴
        
    #. DB 연결 종료
    cur.close()
    conn.close() 
    
    #. Today기준으로 Year,WeekNum 가져오기
    n       = datetime.datetime.now()
    Year    = n.isocalendar()[0]
    WeekNum = n.isocalendar()[1]
    
    #. Class style 배열 정의
    style = ['primary','secondary','info','warning','danger','success','light','dark']
    
    ##. groupby를 통해 각 본부별 해당하는 각 센터에 대한 HTML작성 ##
    #. 결과저장을 위한 빈공간
    result_str = ""
    #. 본부단위로 그룹화
    Result_grouped = Result.groupby(['div1'], sort=True)
    for name, group in Result_grouped:
        div1_str = name
        div2_str = ""
        i=0

        for row_index, row in group.iterrows():
            #. 태그 만들기
            str = """<a href="/report/report_main/{Year}/{WeekNum}/{div_list_id}/{div1}/{div2}" class="btn btn-outline-{style}">{CenterName}</a>""".format(
                Year        = Year,
                WeekNum     = WeekNum,
                div_list_id = row["id"],
                div1        = row["div1"],
                div2        = row["div2"],
                style       = style[i%8],
                CenterName  = row["div2"],
                )
            #. Active Class 추가(센터명 일치시)
            if row["div2"] == div2:
                str = str.replace('class="btn','class="active btn')
            #. 한줄 내리기
            str += '\n'
            #. 추가하기
            div2_str += str
            #. 횟수늘리기
            i += 1
        
        result_str += GetBaseHtml(div1=div1_str, div2=div2_str)
        result_str += '\n'
        
    #. 데이터 저장
    df_Raw["df"] = result_str
        
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    df_Raw["processtime(ms)"] = processtime
        
    return df_Raw
    










