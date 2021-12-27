# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 14:43:09 2021

@author: hicor
"""

#%%
import pandas as pd
from bs4 import BeautifulSoup
import timeit
import os
import psycopg2
import datetime
import psycopg2.extras as extras
from datetime import timezone, timedelta, datetime
import pytz

#%% DB 연결정보
DB_CONN = {'host'     :os.environ.get("SQL_HOST",     "3.37.42.132"),
           'dbname'   :os.environ.get("SQL_DATABASE", "report"),
           'user'     :os.environ.get("SQL_USER",     "hicor"),
           'password' :os.environ.get("SQL_PASSWORD", "dlacodnr1!"),
           'port'     :os.environ.get("SQL_PORT",     "4040"),
           'options'  :'-c search_path=dbo,public'}

#%%해당 부서&년도&주자에 맞는 보고 템플릿 불러오기

def get_template_info(div_list_id, Year, WeekNum):
    #. DB 연결 열기
    conn = psycopg2.connect(host     = DB_CONN['host'],
                            dbname   = DB_CONN['dbname'],
                            user     = DB_CONN['user'],
                            password = DB_CONN['password'],
                            port     = DB_CONN['port'],
                            options  = DB_CONN['options'])
    cur = conn.cursor()
    
    #. 쿼리변수 정의
    TableName = "report_template_list"
    SELECT   = "*" 
    LIMIT     = "999"
    
    #. 쿼리조합 ( concat은 문자열 합치기 ) # 유사한 경우도 포함하여 쿼리한다. 
    SQL = """
        SELECT     {SELECT}
        FROM       "{TableName}"
        WHERE      "Year" = {Year} and "WeekNum" = {WeekNum} and "div_list_id" = {div_list_id}
        LIMIT       {LIMIT}
        """.format(
        SELECT      = SELECT,
        TableName   = TableName,
        Year        = Year,
        WeekNum     = WeekNum,
        div_list_id = div_list_id,
        LIMIT       = LIMIT
        )
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        Result = pd.read_sql(SQL, conn)
    except:
        Result = pd.DataFrame() # 빈 데이터 프레임 리턴
        
    #. 템플릿 이름 리턴
    try:
        TemplateName = Result["TemplateName"][0]
    except:
        TemplateName = "표준_2021_1.xlsx"
        
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    return TemplateName


#%% 주간업무보고 내용 불러오기
def GetRegisteredReport(div_list_id, Year, WeekNum):
    #div_list_id = 1
    #Year= 2021
    #WeekNum = 26
    #. DB 연결 열기
    conn = psycopg2.connect(host     = DB_CONN['host'],
                            dbname   = DB_CONN['dbname'],
                            user     = DB_CONN['user'],
                            password = DB_CONN['password'],
                            port     = DB_CONN['port'],
                            options  = DB_CONN['options'])
    cur = conn.cursor()
    
    #. 쿼리변수 정의
    TableName    = "report_list"
    SELECT       = "*" 
    Year         = Year
    WeekNum      = WeekNum
    div_list_id  = div_list_id
    
    LIMIT     = "999"
    
    #. 쿼리조합 ( concat은 문자열 합치기 ) # 유사한 경우도 포함하여 쿼리한다. 
    SQL = """
        SELECT     {SELECT}
        FROM       "{TableName}"
        WHERE      "Year" = {Year} and "WeekNum" = {WeekNum} and "div_list_id" = {div_list_id}
        ORDER BY    등록일시 desc
        LIMIT       {LIMIT}
        """.format(
        SELECT      = SELECT,
        TableName   = TableName,
        Year        = Year,
        WeekNum     = WeekNum,
        div_list_id = div_list_id,
        LIMIT       = LIMIT
        )
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        Result = pd.read_sql(SQL, conn)
    except:
        Result = pd.DataFrame() # 빈 데이터 프레임 리턴
        
        
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    return Result

#%% 주간업무보고 내용을 텍스트로 변환하고 정리해주는 모듈

def GetString(Result, index, Div, UserID):
    
    #index = 1
    #Div = "Performance"
    dt        = datetime.now(timezone.utc)
    timestamp = dt.astimezone()
    오늘날짜  = timestamp.date()  #datetime.date(datetime.now())
    
    data = Result[(Result["ContentsID"]==index) & (Result["Div"]==Div)]
    string="" # TextArea에서 입력한 white space가 인식되도록 스타일 설정
    for index, row in data.iterrows():
        
        #. 중요도에 따라서 강조여부 삽입
        if row["중요도"] == '높음':
            string +="<div style='font-weight:600;'>"
        else:
            string +="<div>"
        
        ####.제목 정보 ####
        string += "<p style='margin-bottom:1px;'>"
        #1. 금액 정보 추가하기
        if row["금액"] > 0.0: # 금액이 존재하는 경우 구분
            string += '∘ {제목} [{금액} {단위}]'.format(제목=row["제목"],금액=row["금액"],단위=row["단위"])
        else: # 금액이 존재하지 않는 경우
            string += '∘ {제목}'.format(제목=row["제목"])
        
        #2. 장소&업체 정보 추가하기
        if row["장소업체"]: # 장소업체가 존재하는 경우 구분
            string += '({장소업체}, {담당자})'.format(장소업체=row["장소업체"],담당자=row["담당자"])
        else: # 장소업체가 존재하지 않는 경우 구분
            string += '({담당자})'.format(담당자=row["담당자"])
            
        #3. 날짜 정보 추가하기
        if row["시작일"] == row["종료일"]: # 시작과 종료일이 같은 경우,
            string += '({시작일})'.format(시작일=row["시작일"])
        else: # 시작과 종료일이 다른 경우,
            string += '({시작일}~{종료일})'.format(시작일=row["시작일"], 종료일=row["종료일"])
            
            
        #4. "new"버튼 만들기 _ 현재시간과 비교해서 new표기 등록

        #(1). 서울(한국)시간으로 변경해주기 ( utc + 9시간 )
        try:# 가끔 시간정보가 이상하게 들어간놈(더미데이터)가 있어서 예외처리 일단추가..
            등록일시 = row["등록일시"].astimezone(pytz.timezone('Asia/Seoul')).date()
        except:
            등록일시 = ""
            
        #(2). 등록일과 오늘날짜가 같은경우, (new)표기를 추가한다.
        if 오늘날짜 == 등록일시 :
            string += '<code>(New)</code>'
        else:
            pass
            
        #5. "수정"버튼 만들기 _ 작성자ID와 request요청한 ID를 비교하여 (수정)버튼을 추가한다. (백업)<span type='button' class='badge bg-light' onClick="GetReportDetail(this, ReportID='{ReportID}')">수정</span>
        #(참고)https://coding-factory.tistory.com/192
        if UserID == str(row["작성자ID"]): 
            string += """
            <i type='button' class='fas fa-cog fa-spin' style='color: #0d6efd8c; height: 14px;' onClick="GetReportDetail(this, ReportID='{ReportID}')"></i>
            """.format(ReportID=row["id"])
        else:
            pass

        #6. 제목 닫기
        string +="</p>"
        
        ####. 내용 정보 ####
        string += "<p style='white-space:pre; margin-bottom:10px; padding-left:10px;'>" # TextArea에서 입력한 white space가 인식되도록 스타일 설정 + paddin으로 들여쓰기
        string += row["내용"]
        string +="</p>"
        

        #. 내용 닫기
        string += '</div>'

    return string


#%% 주간업무보고 데이터 HTML양식에 맞게 불러오기

def CallReportTemplate(div_list_id, Year, WeekNum, UserID):
    #. 빈데이터 생성
    df_Raw={}
    
    #. 현재 년도 & 주차 & 요청부서
    Year        = Year #2021 
    WeekNum     = WeekNum #20
    div_list_id = div_list_id # 2
    
    #. 시작시간 체크
    tic=timeit.default_timer()
    
    #. 인덱스열 지정 ( 묶음처리 (rowspan, colspan) 할 열을 지정)
    #index_col = ['index','전략방향', '전략과제', '세부과제']
    index_col = ['전략방향', '전략과제', '세부과제']
    
    #. 해당 부서&년도&주자에 맞는 보고 템플릿 불러오기
    #. (참고) 존재하지 않는경우, 표준_2021_1.xlsx 으로 지정
    TemplateName = get_template_info(div_list_id, Year, WeekNum)
    
    #. 템플릿 경로 만들기
    ProjectPath  = os.getcwd()
    addPath      = "app/Utils/Report"
    BasePath     = os.path.join(ProjectPath, addPath)
    TotalPath    =  os.path.join(BasePath, TemplateName)
    
    ###. 테이블 불러오기
    df = pd.read_excel(TotalPath, engine="openpyxl")
    
    ###. 저장된 주간업무보고 사항 불러오기
    Result = GetRegisteredReport(div_list_id, Year, WeekNum)
    
    #. 인덱스(숫자)부여
    df = df.reset_index()
    #. 인덱스로 지정된 열에 대해 병합된 또는 비어있는 셀값을 위의값으로 채워준다.
    df[index_col] = df[index_col].fillna(method='ffill') 
    #. 인덱스로 지정되지 않은 열애 대해 비어있는 셀값을 "-"로 채워준다.
    df["구분"] = df["구분"].fillna('[None]') 
    #. HTML에서 쉽게 병합하기위해 병합이 필요한 열을 index 지정한다.
    df = df.set_index(index_col) 
    #. df를 html로 변환
    html = df.to_html(classes='mytable') 

    #. 변환된 html을 사용하기 tbody만 추출한다.
    soup   = BeautifulSoup(html, "html.parser")
    target = soup.find('tbody')

    #. 각 행을 순환하면서 필요한 정보를 추가한다.
    trs = target.findAll("tr")
    i=0
    for tr in trs:
        #. index열은 Hidden해야하므로, class를 부여하고, 추후 style="display:none;" 을 부여한다.
        #. Set attribute 기능을 이용하여 index열에 class 부여
        tr.findAll("td")[0].attrs["class"] = "hidden"
        tr.findAll("td")[0].attrs["TemplateName"] = TemplateName
        tr.findAll("td")[0].attrs["id"] = i
        
        ##. 실적 & 계획 데이터 열 추가##
        last_td = tr.findAll("td")[1] #. 마지막 td에 열을 추가해야하므로 마지막 td 저장(구분 열)
        #1.td태그 생성
        Plan        = soup.new_tag('td', href='#', id='link1', style="vertical-align : top;", **{'class':'Plan'})
        Performance = soup.new_tag('td', href='#', id='link1', style="vertical-align : top;", **{'class':'Performance'})
        #2. (선택사항)문자추가
        Plan.string        = ""
        Performance.string = ""
        #3. 적용 (insert_after: 태그바로뒤에 태그 추가 )
        last_td.insert_after(Plan)
        last_td.insert_after(Performance)
        
        ##. 추가된 실적 & 계획 데이터 열에 주간업무보고 데이터 및 템플릿 정보가 포함된 "Add버튼"추가
        Performance_col = tr.findAll("td")[2] #. 실적 열
        Plan_col        = tr.findAll("td")[3] #. 실적 열
        
        #1. 주간업무보고내용 추가
        Performance_col.append(BeautifulSoup(GetString(Result, index = i, Div = "Performance", UserID=UserID), 'html.parser'))
        Plan_col.append(BeautifulSoup(GetString(Result, index = i, Div = "Plan", UserID=UserID), 'html.parser'))

        #2.button태그 생성 (백업)  <button class="btn icon btn-primary" onClick="Popmodal(sep1='{sep1}', sep2='{sep2}', sep3='{sep3}', sep4='{sep4}', TemplateName='{TemplateName}', Year='{Year}', WeekNum='{WeekNum}', id='{id}', Div='{Div}')"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg></button>
        Button_Tag_Base = """
        <div></div>
        <span class="fas fa-pencil-alt fa-lg" style='color: #39da8a;' type='button' onClick="Popmodal(sep1='{sep1}', sep2='{sep2}', sep3='{sep3}', sep4='{sep4}', TemplateName='{TemplateName}', Year='{Year}', WeekNum='{WeekNum}', id='{id}', Div='{Div}')"></span>
        """.format(sep1=df.index[i][0], sep2=df.index[i][1], sep3=df.index[i][2], sep4=df["구분"][i], TemplateName=TemplateName, Year=Year, WeekNum=WeekNum, id=i,  Div="Select" )

        #3.Div에 맞게 변경하여 Append로 적용 (append: 태그안에 태그 추가 )
        Performance_col.append(BeautifulSoup(Button_Tag_Base.replace("Div='Select'", "Div='Performance'"), 'html.parser'))
        Plan_col.append(BeautifulSoup(Button_Tag_Base.replace("Div='Select'", "Div='Plan'"), 'html.parser'))
        
        #.4 루프카운트 증가
        i += 1


    #. 수정된 tbody안에 있는 tr(행)들을 df에 저장
    df_Raw["df"] = str(trs)
    
    
    #.(21.07.06추가) 보고서 등록사람 df에 저장
    df_Raw["RegisterdedPerson"] = GetRegisterdedPerson(div_list_id, Year, WeekNum)
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    df_Raw["processtime(ms)"] = processtime
    
    return df_Raw


#%% 주간업무보고 사항을 DB에 저장

def ReportRegist(data):
    
    #. 빈데이터 생성
    df_Raw={}
    
    #. 시작시간 체크
    tic=timeit.default_timer()

    #. 저장 테이블 및 데이터 정보 받기
    #.(샘플)data = {'csrfmiddlewaretoken': 'O7SiMbfgXSpaATbBxlUIWHip7P61T40DnYDG4INJ5lOJqesRqo2hP5CCNXYZAqnP', '제목': 'ㅇㅇㅇㅇㅇㅇ', '내용': 'ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ', '담당자': 'ㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇㅇ', '장소업체': '', '금액': '0.0', '단위': '백만원', '출장여부': '일반', '중요도': '일반', '시작일': '2021/06/23', '종료일': '2021/06/23', 'TemplateName': '표준_2021_1.xlsx', 'ContentsID': '0', 'Div': 'Performance', 'Year': '2021', 'WeekNum': '27', '작성자': '임채욱', '작성자ID': '4', 'div_list_id': '1', '등록일시': '2021-07-05T20:30:24.597630+09:00', 'ReportID': '#'}
    data = data
    TableName='report_list'
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = DB_CONN['host'],
                            dbname   = DB_CONN['dbname'],
                            user     = DB_CONN['user'],
                            password = DB_CONN['password'],
                            port     = DB_CONN['port'],
                            options  = DB_CONN['options'])
    cur = conn.cursor()
    
    #.전체데이터 받기
    
    ##. 데이터 클리닝
    #1. csrf제외 
    del data["csrfmiddlewaretoken"]
    
    #2. ReportID제외 (수정할때 사용할거임)
    del data["ReportID"]
    
    #3. 등록일시 업데이트
    dt        = datetime.now(timezone.utc)
    timestamp = dt.astimezone().isoformat()
    #timestamp = dt.astimezone()
    data["등록일시"] = timestamp
    
    #3.df로 변경
    data=pd.DataFrame([data])
    
    ##. SQL 만들기
    #1. INSERT 쿼리 만들기
    NewColumn = []
    for item in data.columns:
        NewColumn.append('"'+item+'"')
    ColStr = ','.join(list(NewColumn))
    ColStr = 'INSERT INTO "{TableName}"' '('.format(TableName=TableName) + '"id",' + ColStr + ')'
    
    #2. VALUES 쿼리 만들기 ( id는 자동추가 되도록 명령 )
    ValStr=""
    tuples = [tuple(x) for x in data.to_numpy()]
    for data in tuples[0]:
        ValStr+="'{}',".format(data)
    ValStr = "VALUES ((SELECT MAX(id)+1 FROM {TableName}), ".format(TableName=TableName) + ValStr[:-1]+")"
    
    #3. 쿼리 합치기
    SQL = ColStr + ValStr
    
    ##. 쿼리 실행
    try: #. 쿼리결과가 없으면 에러발생, 예외처리
        #. 쿼리실행
        test = cur.execute(SQL)
        #. 쿼리 커밋
        conn.commit()
    except:
        test = pd.DataFrame() #. 빈 데이터 프레임 리턴
        print("에러")
    
    
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    df_Raw["processtime(ms)"] = processtime
    df_Raw["Msg"] = "저장완료"
    
    return df_Raw

#%% 주간업무보고 Detail 사항 보여주기
def GetReportDetail(ReportID):

    #. 빈데이터 생성
    df_Raw={}
    
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
    TableName    = "report_list"
    SELECT       = "*" 
    ReportID     = ReportID
    LIMIT        = "1"
    
    #. 쿼리조합 ( concat은 문자열 합치기 ) # 유사한 경우도 포함하여 쿼리한다. 
    SQL = """
        SELECT     {SELECT}
        FROM       "{TableName}"
        WHERE      "id" = {ReportID}
        LIMIT       {LIMIT}
        """.format(
        SELECT      = SELECT,
        TableName   = TableName,
        ReportID    = ReportID,
        LIMIT       = LIMIT
        )
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        Result = pd.read_sql(SQL, conn)
    except:
        Result = pd.DataFrame() # 빈 데이터 프레임 리턴
        
        
    #. 등록일시정보( timestamp with time zone)은 JSON변경시 문제가 있으므로 일단 제외
    del Result["등록일시"]
    
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    df_Raw["processtime(ms)"] = processtime
    df_Raw["df"] = Result
    
    return df_Raw

#%%주간업무보고 삭제하기
def ReportDelete(ReportID):

    #. 빈데이터 생성
    df_Raw={}
    
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
    TableName    = "report_list"
    ReportID     = ReportID

    
    #. 쿼리조합 ( concat은 문자열 합치기 ) # 유사한 경우도 포함하여 쿼리한다. 
    SQL = """
        DELETE
        FROM   "{TableName}"
        WHERE  "id" = {ReportID}
        """.format(
            TableName = TableName,
            ReportID  = ReportID
            )
    
    ##. 쿼리 실행
    try: #. 쿼리결과가 없으면 에러발생, 예외처리
        #. 쿼리실행
        Result = cur.execute(SQL)
        #. 쿼리 커밋
        conn.commit()
    except:
        Result = pd.DataFrame() #. 빈 데이터 프레임 리턴
        print("에러")
    
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    df_Raw["processtime(ms)"] = processtime
    df_Raw["df"] = pd.DataFrame() #. 빈 데이터 프레임 리턴
    
    return df_Raw

#%% 주간업무보고 사항을 수정(UPDATE)하기

def ReportModify(data):
    
    #. 빈데이터 생성
    df_Raw={}
    
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
    
    #. 저장 테이블 및 데이터 정보 받기
    #(샘플)data = {'csrfmiddlewaretoken': 'ee9opTG7fl0aU8W95h9D6CTrAilyIPyOJZhyPLex5oI4PekJdXQny8wbOssNZaqL', '제목': 'adada', '내용': 'wdadawda', '담당자': 'wdawd', '장소업체': '', '금액': '0.0', '단위': '백만원', '출장여부': '일반', '중요도': '일반', '시작일': '2021-06-22', '종료일': '2021-06-22', 'TemplateName': '표준_2021_1.xlsx', 'ContentsID': '0', 'Div': 'Plan', 'Year': '2021', 'WeekNum': '27', '작성자': '임채욱', '작성자ID': '4', 'div_list_id': '1', '등록일시':"#", 'ReportID': '22'}
    data = data
    TableName='report_list'
    
    #. 등록일시 업데이트
    dt        = datetime.now(timezone.utc)
    timestamp = dt.astimezone().isoformat()
    #timestamp = dt.astimezone()
    data["등록일시"] = timestamp
    
    #. csrf데이제터 제거
    del data["csrfmiddlewaretoken"]
    #. ReportID 제거 저( 저장 후 제거 )
    ReportID = data["ReportID"]
    del data["ReportID"]
    

    #.SQL만들기
    SetString = ""
    for key, val in data.items():
        SetString += '"' + key + '"'
        SetString += '='
        SetString += "'" + val + "'"
        SetString += ','
    SetString = SetString[:-1]
        
        
    SQL = """
        UPDATE "{TableName}"
        SET    {SetString}
        WHERE  id = {ReportID}
    """.format(
            TableName = TableName,
            SetString = SetString,
            ReportID   = ReportID
            )
    
    ##. 쿼리 실행
    try: #. 쿼리결과가 없으면 에러발생, 예외처리
        #. 쿼리실행
        test = cur.execute(SQL)
        #. 쿼리 커밋
        conn.commit()
    except:
        test = pd.DataFrame() #. 빈 데이터 프레임 리턴
        print("에러")
    
    
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    df_Raw["processtime(ms)"] = processtime
    df_Raw["df"] = pd.DataFrame()
    
    return df_Raw

#%% 계획&실적 _ 등록, 미등록자 확인

def GetRegisterdedPerson(div_list_id, Year, WeekNum):
    #div_list_id=1 
    #Year=2021 
    #WeekNum=27

    #. 빈데이터 생성
    df_Raw={}
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = DB_CONN['host'],
                            dbname   = DB_CONN['dbname'],
                            user     = DB_CONN['user'],
                            password = DB_CONN['password'],
                            port     = DB_CONN['port'],
                            options  = DB_CONN['options'])
    cur = conn.cursor()
    
    #########1. 해당 부서의 구성원 가져오기##########
    SQL = """
        SELECT "id","personalnumber","username"
        FROM "auth_user_info" INNER JOIN "auth_user" ON (auth_user_info.personalnumber = auth_user.first_name)
        WHERE "div_id" = '{div_id}'
    """.format(div_id = div_list_id)
    
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        All_member = pd.read_sql(SQL, conn)
    except:
        All_member = pd.DataFrame() # 빈 데이터 프레임 리턴
        
        
    #########2. 보고작성한 사람 가져오기(distinct로 중복제거)########## 
    SQL = """
        SELECT distinct "작성자","작성자ID","Div"
        FROM "report_list"
        WHERE "div_list_id" = '{div_list_id}' and "Year" = '{Year}' and "WeekNum" = '{WeekNum}'
    """.format(
            div_list_id = div_list_id,
            Year = Year,
            WeekNum = WeekNum)
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        Selected_member = pd.read_sql(SQL, conn)
    except:
        Selected_member = pd.DataFrame() # 빈 데이터 프레임 리턴
        
        
    #########3. 분류에 맞게 데이터 정리########## 
    #1) 실적-등록
    df_Raw["실적_등록"] = sorted(Selected_member[Selected_member['Div']=='Performance']['작성자'].tolist())
    #2) 계획-등록
    df_Raw["계획_등록"] = sorted(Selected_member[Selected_member['Div']=='Plan']['작성자'].tolist())
     
    #3) 실적-미등록
    Performance_merge = pd.merge(left = All_member , right = Selected_member[Selected_member['Div']=='Performance'], how = "outer", left_on = "id", right_on = "작성자ID")
    Plan_merge = pd.merge(left = All_member , right = Selected_member[Selected_member['Div']=='Plan'], how = "outer", left_on = "id", right_on = "작성자ID")
    
    df_Raw["실적_미등록"] = sorted(Performance_merge[Performance_merge['작성자'].isnull()]['username'].tolist())
    df_Raw["계획_미등록"] = sorted(Plan_merge[Plan_merge['작성자'].isnull()]['username'].tolist())
       
    
    #. DB 연결 종료
    cur.close()
    conn.close()

    return df_Raw

