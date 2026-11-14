FROM nginx:1.27-alpine

# o volume é escrito pelo jenkins (uid 1000), então a pasta já nasce vazia e com esse dono
RUN rm -rf /usr/share/nginx/html/* && chown 1000:1000 /usr/share/nginx/html

COPY default.conf /etc/nginx/conf.d/default.conf
