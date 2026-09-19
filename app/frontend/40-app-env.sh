#!/bin/sh
set -e

if [ -n "$APP_ENV" ]; then
  APP_ENV_LABEL=" — $APP_ENV"
else
  APP_ENV_LABEL=""
fi

export APP_ENV_LABEL

envsubst '${APP_ENV_LABEL}' \
  < /usr/share/nginx/html/index.template.html \
  > /usr/share/nginx/html/index.html