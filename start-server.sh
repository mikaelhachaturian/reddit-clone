#!/bin/bash

(cd reddit-clone; gunicorn reddit_clone.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
