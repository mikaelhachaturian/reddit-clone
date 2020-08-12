FROM python:3.7-alpine

RUN apk update && apk add nginx build-base
COPY nginx/nginx.default /etc/nginx/sites-available/default
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN \
  mkdir -p /opt/app/reddit-clone && \
  mkdir -p /run/nginx && \
  mkdir -p /etc/nginx/sites-enabled/ && \
  ln -sf /dev/stdout /var/log/nginx/access.log && \
  ln -sf /dev/stderr /var/log/nginx/error.log && \
  ln -s /etc/nginx/sites-available/default  /etc/nginx/sites-enabled/default

COPY docker/* /opt/app/
COPY reddit-clone /opt/app/reddit-clone/
WORKDIR /opt/app
RUN \
  adduser -D -H -u 1000 -s /bin/bash www-data -G www-data && \
  chown -R www-data:www-data /opt/app
RUN pip3 install -r requirements.txt

EXPOSE 8020
CMD ["/opt/app/start-server.sh"]