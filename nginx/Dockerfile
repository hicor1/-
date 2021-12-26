FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# 21.4.30 추가 : SSL 마운트
COPY WILD.ktl.re.kr.crt.pem /etc/nginx/WILD.ktl.re.kr.crt.pem
COPY WILD.ktl.re.kr.key.pem /etc/nginx/WILD.ktl.re.kr.key.pem