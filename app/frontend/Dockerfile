FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.template.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY 40-app-env.sh /docker-entrypoint.d/40-app-env.sh