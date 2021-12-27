import timeit
import psycopg2
import pandas as pd
import datetime
import os

ConnectInfo = {'host'     :os.environ.get("SQL_HOST",     "3.37.42.132"),
               'dbname'   :os.environ.get("SQL_DATABASE", "report"),
               'user'     :os.environ.get("SQL_USER",     "hicor"),
               'password' :os.environ.get("SQL_PASSWORD", "dlacodnr1!"),
               'port'     :os.environ.get("SQL_PORT",     "4040"),
               'options'  :'-c search_path=dbo,public'}

#%% 모듈
#. 리턴할 데이터 칼럼 리스트(SELECT) 스트링 변환  
def GetColumnString(ColumnList): # ex: "StandarDesignation","TestMethod","TestRange"
    text = ""
    if ColumnList == '*':
        text = '*'
    else:
        for Column in ColumnList:
            text += ","
            text += '"'
            text += Column
            text += '"'
        text = text[1:] # ,는 불필요하므로 삭제
        text = 'DISTINCT' + text # 중복데이터 방지를 위해, Select된 열기준으로 중복항 제거
    return text

# 종합검색이 아닌, 특정열을 지정한 검색
def GetSpecificQueryString(QueryDict): 

    text = ""
    for key, val in QueryDict.items():
        text += " AND "
        text += '"' + key + '"'
        text += " ILIKE "
        text += "'%" + val + "%'"
    
    text = text[4:] #AND제거
    
    return text

#. 쿼리와 검색열을 ILIKE를 이용하여 대소문자 구분없이색, 자체 효율은 낮으나, index와 함께 사용할 경우 효율 대폭 상승
def GetQueryString(Target, Query): # ex: concat("StandarDesignation","TestMethod","TestRange") ILIKE '%KS%' AND concat("StandarDesignation","TestMethod","TestRange") ILIKE '%210:2018%'
    Query = Query.replace("-"," ") # 교정 기술지원코드에서 bar 제거
    Query = Query.split()
    Query = [item for item in Query if len(item) >= 2] # 두 글자 이상인 쿼리(키워드)사용
    
    text = ""
    for string in Query:
        text += " AND " # 확실히 OR보다는 AND가 겁색속도가 빠름
        text += Target
        text += " LIKE " # 검색대상 및 질의어 모두 소문자로 변환했으므로 ilike(x), like(o) 개꿀, 검색 속도 개선됨
        text += "'%" # 쿼리문 양쪽에 %를 포함하면, contain조건이 됨
        text += string
        text += "%'"
    text = text[4:] # AND는 불필요하므로 삭제
    
    return text

#print(GetQueryString(Target="제목", Query="위탁 전산"))

#%% 회원가입정보 입력

def AuthRegist(사번, 부서1, 부서2, 기타):
    
    #. 시작시간 체크
    tic=timeit.default_timer()
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = ConnectInfo['host'],
                            dbname   = ConnectInfo['dbname'],
                            user     = ConnectInfo['user'],
                            password = ConnectInfo['password'],
                            port     = ConnectInfo['port'],
                            options  = ConnectInfo['options'])
    cur = conn.cursor()
    
    ######################################################
    ######. 해당 부서정보를 기준으로 부서 ID 받아오기#######
    #####################################################
    SQL = """
        SELECT "id"
        FROM "div_list"
        WHERE "div1"='{div1}' and "div2"='{div2}'
    """.format(div1=부서1, div2=부서2)

    try: #. 쿼리결과가 없으면 에러발생, 예외처리
        #. 쿼리실행
        test = pd.read_sql(SQL, conn)
    except:
        test = pd.DataFrame() # 빈 데이터 프레임 리턴
        print("에러1")
    
    #. 부서 id 정보 저장
    div_id = test['id'][0]

    ######################################################
    ######. 가입정보 저장하기                       #######
    #####################################################
    
    #. 쿼리조합 ( concat은 문자열 합치기 )
    #. ID 자동증가 : VALUES ((SELECT MAX(id)+1 FROM auth_user_info), '150010', '산업표준본부', '공업물리표준센터', '유체유동팀')
    SQL = """
        INSERT INTO "auth_user_info"("personalnumber","부서1","부서2","기타","div_id")
        VALUES ('{사번}', '{부서1}', '{부서2}', '{기타}', '{div_id}')
        RETURNING *;
    """.format(
            사번     = 사번,
            부서1    = 부서1,
            부서2    = 부서2,
            기타     = 기타,
            div_id   = div_id
        )
        
    try: #. 쿼리결과가 없으면 에러발생, 예외처리
        #. 쿼리실행
        test = cur.execute(SQL)
        #. 쿼리 커밋
        conn.commit()
    except:
        test = pd.DataFrame() #. 빈 데이터 프레임 리턴
        print("에러2")
    
    

    #. DB 연결 종료
    cur.close()
    conn.close()
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    return {"processtime(ms)" : processtime,
            "df"              : test}

#test = AuthRegist(사번="150010", 부서1="산업표준본부", 부서2="공업물리표준센터", 기타="유체유동팀")

#%% 회원가입 ( 중복 ) 점검

def Auth_Duplicate_check(사번, username, email):
    #사번     = '150010'
    #username = '임채욱'
    
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = ConnectInfo['host'],
                            dbname   = ConnectInfo['dbname'],
                            user     = ConnectInfo['user'],
                            password = ConnectInfo['password'],
                            port     = ConnectInfo['port'],
                            options  = ConnectInfo['options'])
    cur = conn.cursor()
    
    #. auth_user 테이블과 auth_user_info 테이블을 조인해서 가져온다.
    SQL = """
        SELECT *
        FROM auth_user, auth_user_info
        WHERE personalnumber = '{사번}' OR username = '{username}' OR email = '{email}'
    """.format(사번=사번, username=username, email=email)
    
    Query = pd.read_sql(SQL, conn).shape[0]
    
    if Query <= 0:
        Duplicate = False
    else:
        Duplicate = True
    
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    return Duplicate

#%% 사번으로 "auth_user_info" 정보 조회하기

def Get_user_info(사번):
    #사번     = '150010'
    #username = '임채욱'
    
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = ConnectInfo['host'],
                            dbname   = ConnectInfo['dbname'],
                            user     = ConnectInfo['user'],
                            password = ConnectInfo['password'],
                            port     = ConnectInfo['port'],
                            options  = ConnectInfo['options'])
    cur = conn.cursor()
    
    #. auth_user 테이블과 auth_user_info 테이블을 조인해서 가져온다.
    SQL = """
        SELECT *
        FROM auth_user_info
        WHERE personalnumber = '{사번}' 
    """.format(사번=사번)
    
    Result = pd.read_sql(SQL, conn)
    

    #. DB 연결 종료
    cur.close()
    conn.close()
    
    return Result

Result = Get_user_info(사번='150010')['부서1'][0]

#%% 조건 일반검색
def DBSpecificQuery(ConnectInfo, TableName, ColumnList, QueryDict, SortField, Sortby, Limit):

    #. 시작시간 체크
    tic=timeit.default_timer()
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = ConnectInfo['host'],
                            dbname   = ConnectInfo['dbname'],
                            user     = ConnectInfo['user'],
                            password = ConnectInfo['password'],
                            port     = ConnectInfo['port'],
                            options  = ConnectInfo['options'])
    cur = conn.cursor()
    
    #. 쿼리변수 정의
    QueryDict = QueryDict
    From      = TableName
    Limit     = Limit
    
    #. 쿼리조합 ( concat은 문자열 합치기 )  ex) : OrderBy = "similarity" DESC, "AccreditName" ASC
    SQL = """
        SELECT      {0}
        FROM       "{1}"
        WHERE       {2}
        ORDER BY   "{3}" {4}
        LIMIT       {5}
        """.format(GetColumnString(ColumnList), From, GetSpecificQueryString(QueryDict), SortField, Sortby, Limit)
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        test = pd.read_sql(SQL, conn)
    except:
        test = pd.DataFrame() # 빈 데이터 프레임 리턴
    

    #. DB 연결 종료
    cur.close()
    conn.close()
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    #print(SQL)
    
    return {"processtime(ms)":processtime,
            "df" : test}


#%% (유사도 검색)

def Title_Sim_Query(ConnectInfo, Query, ContentsID, div_list_id):

    #. 시작시간 체크
    tic=timeit.default_timer()
    
    #. DB 연결 열기
    conn = psycopg2.connect(host     = ConnectInfo['host'],
                            dbname   = ConnectInfo['dbname'],
                            user     = ConnectInfo['user'],
                            password = ConnectInfo['password'],
                            port     = ConnectInfo['port'],
                            options  = ConnectInfo['options'])
    cur = conn.cursor()

    #. 쿼리조합 ( concat은 문자열 합치기 )  ex) : OrderBy = "similarity" DESC, "AccreditName" ASC
    SQL = """
        SELECT      "제목","ContentsID","div_list_id","count", similarity("{Target}", '{Query}') 
        FROM       "{From}"
        WHERE       "count" >= 1 AND "ContentsID" = '{ContentsID}' AND "div_list_id" ='{div_list_id}' AND {QueryString}
        ORDER BY   "similarity" DESC, "{SortField}" {Sortby}
        LIMIT       {Limit}
        """.format(
            Target      = "제목",
            Query       = Query,
            QueryString = GetQueryString(Target="제목", Query=Query),
            From        = "제목_카운트",
            ContentsID  = ContentsID,
            div_list_id = div_list_id,
            SortField   = "count",
            Sortby      = "desc",
            Limit       = 10
        )
    
    try: # 쿼리결과가 없으면 에러발생, 예외처리 ㄱㄱ
        test = pd.read_sql(SQL, conn)
        test = test.loc[test["similarity"]>=0.0] # 유사도가 전혀없는 녀석은 제외
    except:
        test = pd.DataFrame() # 빈 데이터 프레임 리턴
    
    #. "제목"만 List로 전달하기
    제목_List = test['제목'].tolist()

    #. DB 연결 종료
    cur.close()
    conn.close()
    
    #. 종료시간 체크
    toc=timeit.default_timer()
    #. 프로세스 시간 산출 (ms)
    processtime = round((toc - tic)*1000,2)
    
    #print(SQL)
    
    return {"processtime(ms)":processtime,
            "df" : 제목_List}

#result = Title_Sim_Query(ConnectInfo, Query = "전산", ContentsID=0, div_list_id=1)

#%% pg_trgm 설치 ( 필요한 경우 만 )
# https://yahwang.github.io/posts/80

def InstallPgtrgm(ConnectInfo):
    #. DB 연결 열기
    conn = psycopg2.connect(host     = ConnectInfo['host'],
                            dbname   = ConnectInfo['dbname'],
                            user     = ConnectInfo['user'],
                            password = ConnectInfo['password'],
                            port     = ConnectInfo['port'],
                            options  = ConnectInfo['options'])
    cur = conn.cursor()
    
    cur.execute('CREATE EXTENSION pg_trgm') 
    cur.execute('CREATE EXTENSION btree_gin')
    conn.commit()
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    print('{} : CREATE EXTENSION pg_trgm Done'.format(datetime.datetime.now()))
    
#InstallPgtrgm(ConnectInfo)

#%% 특정 테이블에 GIN or GIST index(색인)열 생성 ( 필요한 경우 만 ) # 검색열(TargetLIst)과 완전히 일치하는 index를 만들어야 효율 증대!!!
def CreateIndex(ConnectInfo):
    #. DB 연결 열기
    conn = psycopg2.connect(host     = ConnectInfo['host'],
                            dbname   = ConnectInfo['dbname'],
                            user     = ConnectInfo['user'],
                            password = ConnectInfo['password'],
                            port     = ConnectInfo['port'],
                            options  = ConnectInfo['options'])
    cur = conn.cursor()
    
    
    #. 기존 index지우기
    cur.execute('DROP INDEX Title_recommand_idx')
    
    
    #. 새로운 index 생성
    cur.execute('CREATE INDEX Title_recommand_idx    ON "report_list"   USING GIST (( "제목" ) gist_trgm_ops)') # 실제로 이것밖에 안씀

    #.커밋
    conn.commit()
    
    #. DB 연결 종료
    cur.close()
    conn.close()
    
    print('{0} : CREATE INDEX Done'.format(datetime.datetime.now()))
    
#CreateIndex(ConnectInfo)

#%%
if __name__ == "__main__":
    df = AuthRegist()