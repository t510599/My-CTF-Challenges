FROM ubuntu:24.04

ENV domain hitcon

RUN apt-get update && apt-get install -y \
    openssh-server \
    nis

RUN mkdir -p /run/sendsigs.omit.d
RUN mkdir -p /var/run/sshd

RUN echo ${domain} >> /etc/defaultdomain

RUN cat <<EOF >> /etc/rc.local
service rpcbind start
sleep 3
ypbind
/usr/sbin/sshd -D
EOF

RUN userdel -r ubuntu

RUN echo "+::::::" >> /etc/passwd
RUN echo "+:::" >> /etc/group

RUN echo "ypserver node10" >> /etc/yp.conf

RUN sed -i -e 's/passwd:         files/passwd:         files nis/' /etc/nsswitch.conf
RUN sed -i -e 's/group:          files/group:          files nis/' /etc/nsswitch.conf
RUN sed -i -e 's/shadow:         files/shadow:         files nis/' /etc/nsswitch.conf
RUN sed -i -e 's/gshadow:        files/gshadow:        files nis/' /etc/nsswitch.conf

RUN printf 'Match Group webuser\nForceCommand internal-sftp' >> /etc/ssh/sshd_config
RUN sed -i -e 's/#UseDNS no/UseDNS no/' /etc/ssh/sshd_config

RUN echo "/dev/sda1 /       ext4    defaults    0 0" > /etc/fstab
RUN echo "node10:/home/webuser  /home/webuser   nfs   defaults,timeo=900,retrans=5,_netdev      0 0" >> /etc/fstab

CMD ["/bin/bash", "/etc/rc.local"]