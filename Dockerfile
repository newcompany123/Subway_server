# docker build -t smallbee3/subway:base -f Dockerfile.base .

FROM        smallbee3/subway:base
MAINTAINER  smallbee3@gmail.com

ENV         BUILD_MODE  prod
ENV         DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}

# 소스 폴더 전체를 복사
COPY        .   /srv/project

# nginx 설정 파일을 복사 및 링크
RUN         cp -f   /srv/project/.config/${BUILD_MODE}/nginx.conf      /etc/nginx/nginx.conf
RUN         cp -f   /srv/project/.config/${BUILD_MODE}/nginx-app.conf  /etc/nginx/sites-available/
RUN         rm -f   /etc/nginx/sites-enalbed/*
RUN         ln -sf  /etc/nginx/sites-available/nginx-app.conf          /etc/nginx/sites-enabled/

# supervisor 설정 파일을 복사
RUN         cp -f   /srv/project/.config/${BUILD_MODE}/supervisord.conf /etc/supervisor/conf.d/

# pkill nginx로 nginx 종료 후 supervisord -n 실행
CMD         pkill nginx; supervisord -n
EXPOSE      80