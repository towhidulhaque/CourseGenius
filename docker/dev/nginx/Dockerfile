FROM nginx:1.19.0-alpine
COPY .docker/dev/nginx/dev.conf /etc/nginx/nginx.conf
COPY static /usr/src/app/static/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
