FROM httpd:2.4
COPY index.html /var/www/html/
CMD [ "/usr/sbin/httpd","-D","FOREGROUND" ]
EXPOSE 80