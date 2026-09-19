#!/bin/sh
set -e

envsubst '${APP_ENV}' \
  < /usr/share/nginx/html/index.template.html \
  > /usr/share/nginx/html/index.html
