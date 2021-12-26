
Check out the [post](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx).

(참고)https://aiopen.etri.re.kr/
 
## 욱추가
0. 빌드 : 
docker-compose -f docker-compose.prod.yml up -d --build

1. DB만들기 (잘 안되면 docker-compose -f docker-compose.prod.yml down -v, 후에 다시 build): 
docker-compose -f docker-compose.prod.yml exec db psql --username=hicor --dbname=ktools_prod 
docker-compose -f docker-compose.prod.yml exec db psql --username=hicor --dbname=ktools_dev
2. 마이그레이숀 : 
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations --noinput
3. 마이그레이트 : 
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
4. 슈퍼유저 : 
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
5. 정적파일 모으기
python manage.py collectstatic 
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear

5-1. 참고( 리빌드 루틴 )
(왠만하면 down은 쓰지말자... pgAdmin 서버정보 사라짐) docker-compose -f docker-compose.prod.yml stop
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
docker-compose -f docker-compose.prod.yml up -d --build

6. DB에 접속해보기 ( https://055055.tistory.com/39 ) 참고
docker-compose -f docker-compose.prod.yml exec db /bin/bash
su - postgres
psql --username hicor --dbname ktools_prod  or
psql -h localhost -p 5432 -U hicor -d ktools_prod
\l (DB리스트)
\c hello_django_prod (DB의 테이블 리스트)
\c hello_django_dev (DB의 테이블 리스트)
\d (테이블 목록보기)
\q ( 종료 )
\du (사용자 조회)
7. Log보기
docker-compose -f docker-compose.prod.yml logs -f
8. 컨테이너 삭제 : 
docker-compose -f docker-compose.prod.yml down
9. 이미지 정보보기
docker inspect 9f5e9f3eb127 ( ex: 도커 postgres이미지에서 IP 볼 때도 사용 가능 )
10. 도커 청소(이거 개꿀인듯 ) :
docker system prune

# 도커 컨테이너 네트워크 설정 :
docker network list
docker inspect network #네트워크네임
https://www.daleseo.com/docker-compose-networks/
https://psawesome.tistory.com/75


# 도커 저장 위치 ( in window )
C:\Users\hicor\AppData\Local\Docker\wsl\data

# centos 도커 설치
 - http://lyasee.com/articles/2018-09/CentOS-%EB%8F%84%EC%BB%A4-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0
 - 도커 오프라인(폐쇄망)설치 : https://joonyon.tistory.com/69

# 도커 빌드 및 실행(background)
 - `docker-compose up -d`

# 도커 빌드 및 실행(foreground)
 - `docker-compose up --build`

# docker-composer설치
 - $ sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)- $(uname -m)" -o /usr/local/bin/docker-compose
 - $ sudo chmod +x /usr/local/bin/docker-compose
 - $ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 아래는 필수 !! ( docker-compose 에러가 날경우!)
sudo systemctl start docker
sudo systemctl enable docker

# 이미지 로컬 저장
[리눅스이미지]
docker save k-tools_nginx:latest > C:\Docker_images\LinuxImage\k-tools_nginx.tar
docker save k-tools_web:latest > C:\Docker_images\LinuxImage\k-tools_web.tar
docker save dpage/pgadmin4:latest > C:\Docker_images\LinuxImage\pgadmin4.tar
docker save postgres:12.0-alpine > C:\Docker_images\LinuxImage\postgres.tar

# 이미지 DockerHub Push ( 이미지 이름을 바꿔야되는데 뭔가 꼬일거같은 기분이.. )
docker push hicor1/k-tools_nginx:tagname

# 이미지 로드
[리눅스]
sudo docker load < k-tools_nginx.tar
sudo docker load < k-tools_web.tar
sudo docker load < pgadmin4.tar
sudo docker load < postgres.tar

# 실행중인 컨테이너 확인
(sudo) docker ps -a

# 실행중인 컨테이너 정지 및 삭제
(sudo) docker stop [컨테이너ID]
(sudo) docker rm [컨테이너ID]

# 도커 이미지 삭제
(sudo) docker rmi [이미지ID]

# 도커 컨테이너 생성
(sudo) docker create -it --rm --name [컨테이너 이름] [이미지 이름]:latestsudo 
ex :) sudo docker create --rm --name django_gunicorn django-docker-compose-main_django_gunicorn:latest

# 도커 컨테이너 시작
(sudo) docker start [컨테이너ID or 컨테이너 이름]

# CentOS에 Postgresql설치 ( 폐쇄망 ) _ 잘안되는듯?..
https://hgko1207.github.io/2020/09/10/postgresql-1/

sudo rpm -ivh postgresql11-libs-11.9-1PGDG.rhel7.x86_64.rpm
sudo rpm -ivh postgresql11-11.9-1PGDG.rhel7.x86_64.rpm
sudo rpm -ivh postgresql11-server-11.9-1PGDG.rhel7.x86_64.rpm
sudo rpm -ivh postgresql11-contrib-11.9-1PGDG.rhel7.x86_64.rpm


# Postgresql with Docker
https://luran.me/307


####### SSL 인증서 정리 #############

# .pfx 에서 .crt 추출하기 (.pfx 암호 필요 : Ktl123$$ )
openssl pkcs12 -in WILD.ktl.re.kr.pfx -clcerts -nokeys -out WILD.ktl.re.kr.crt.pem
# .pfx 에서 .key 추출하기 (.pfx 암호 필요 : Ktl123$$ )
openssl pkcs12 -in WILD.ktl.re.kr.pfx -nocerts -nodes -out WILD.ktl.re.kr.key.pem

#. 참고 : https://anomie7.tistory.com/59 , https://elvanov.com/2312
#. 무료 인증서 발급 : https://letsencrypt.org/
#. SSLproxy : https://stackoverflow.com/questions/52547186/changing-ip-of-python-requests
