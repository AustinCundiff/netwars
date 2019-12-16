#!/bin/bash
sed -i "s/IPADDR/$1/g" d.sh
sed -i "s/IPADDR/$1/g" i
sed -i "s/PORT/$2/g" d.sh
sed -i "s/PORT2/$3/g" i
tar zcvf r.tgz i o netstat ps chattr ch deploy.sh
