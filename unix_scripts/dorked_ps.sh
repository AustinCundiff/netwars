#!/usr/bin/bash
args=("$@"); /usr/share/json $@ | egrep -v "ps|json|evil"
