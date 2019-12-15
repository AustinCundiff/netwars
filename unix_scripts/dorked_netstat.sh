#!/usr/bin/bash
args=("$@"); 
netstat $@ | egrep -v "EST"
netstat $@ | grep "EST" | head -1

