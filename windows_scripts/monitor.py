import os, time
from os import system
from prettytable import PrettyTable

def print_connections(addresses, pids):
    print("===============Established Connections===============")
    taskout = os.popen('tasklist /FI "PID eq 4732"').readlines()
    t = PrettyTable(['Address', 'Pid', 'Process'])
    for i in range(len(addresses)):
        for k in range(len(taskout)):
            if len(taskout[3].split(' ')[0]) > 0:
                t.add_row([addresses[i], pids[i], taskout[3].split(' ')[0]])
            #t.add_row([addresses[i], pids[i], ''])
    print(t)

# Get Foreing IPs & associated pids
def gather_connections():
    newaddresses = []
    pids = []
    names = []
    netout = os.popen("netstat -anob").readlines()
    for line in netout:
        if "EST" in line:
            pids.append(line[-6:].strip(' '))
            addr = line[-45:-25].strip(' ').split(':')[0]
            if "127.0.0.1" not in addr:
                newaddresses.append(addr)
    print_connections(newaddresses, pids)
  
def main():
    while(True):   
        gather_connections()
        time.sleep(5)
        system('cls')
main()
    
    
