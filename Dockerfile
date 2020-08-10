FROM python:3.7-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app/reddit-clone
COPY docker/* /opt/app/
COPY reddit-clone /opt/app/reddit-clone/
WORKDIR /opt/app
RUN pip3 install -r requirements.txt
RUN chown -R www-data:www-data /opt/app

EXPOSE 8020
CMD ["/opt/app/start-server.sh"]