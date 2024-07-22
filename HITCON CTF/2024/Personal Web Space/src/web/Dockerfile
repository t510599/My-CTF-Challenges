FROM ubuntu:24.04

ENV domain hitcon

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    apache2 \
    zip \
    nis

RUN mkdir -p /run/sendsigs.omit.d

RUN echo ${domain} >> /etc/defaultdomain
RUN mkdir /var/yp/${domain}

RUN cat <<EOF >> /etc/rc.local
service rpcbind start
sleep 3
ypserv
sleep 5
make -C /var/yp
/usr/sbin/apache2ctl start
cd /app && gunicorn --bind :5000 --access-logfile - --capture-output app:app
EOF

RUN userdel -r ubuntu

RUN groupadd flagholder -g 1500

# Persistent Hash (Flag 2)
# RUN useradd flagholder -u 1500 -g 1500 -N -M -s /usr/sbin/nologin
# RUN echo "flagholder:flagholdersSuper1oooongp4ssw0rd!!" | chpasswd
# RUN passwd --lock flagholder
RUN echo "flagholder:x:1500:1500::/home/flagholder:/usr/sbin/nologin" >> /etc/passwd
RUN echo 'flagholder:!$y$j9T$LNmGE79e0l4Rj6bKhTosA1$rP24Qc3XWuTvNKKn0fes4WWjbcptfskAaRQInBbKIO2:19916:0:99999:7:::' >> /etc/shadow

RUN groupadd webuser -g 2000

RUN sed -i -e 's/MERGE_PASSWD=false/MERGE_PASSWD=true/' /var/yp/Makefile

COPY ./site.conf /etc/apache2/sites-available/000-default.conf
COPY ./dash.conf /etc/apache2/sites-available/dash.conf
RUN a2ensite dash
RUN a2enmod userdir headers proxy proxy_http substitute 
RUN sed -i -e 's/*\/public_html/webuser\/*\/public_html/' /etc/apache2/mods-available/userdir.conf

COPY ./index.html /var/www/html/index.html
COPY ./robots.txt /var/www/html/robots.txt

RUN zip -r /var/www/html/apache2.zip /etc/apache2

COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --break-system-packages

COPY ./app /app

CMD ["/bin/bash", "/etc/rc.local"]