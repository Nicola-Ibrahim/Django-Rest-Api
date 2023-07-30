FROM nginx:1-alpine


# COPY ./default.conf /etc/nginx/conf.d/default.conf


RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d
