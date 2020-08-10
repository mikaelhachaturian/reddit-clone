#!/bin/bash

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd reddit-clone; python3 manage.py createsuperuser --no-input)
fi

(cd reddit-clone; gunicorn reddit_clone.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
