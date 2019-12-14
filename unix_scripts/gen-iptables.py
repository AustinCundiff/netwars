import ipaddress
import sys
import os
import subprocess

#take in a white list and create input and output rules with an explicit deny at the end

def print_rule_input(x):
    print("iptables -A INPUT -p tcp -s " + str(x) + " -j ACCEPT")


def print_rule_output(x):
    print("iptables -A OUTPUT -p tcp -d " + str(x) + " -j ACCEPT")


def print_closure():
    return "iptables -A INPUT -j DROP" + "\n" + "iptables -A OUTPUT -j DROP"


def main(argv):
    whitelist = "whitelist.txt"
    if os.path.exists(whitelist) and os.path.getsize(whitelist) > 0:
        with open(whitelist, 'r') as f:
            w_str = f.read().splitlines()
    else:
        w_str = list(sys.argv[1:])
    x = list(ipaddress.IPv4Network(u'10.2.1.0/24'))[1:-1]
    for ip in x:
        if str(ip) in w_str:
            input_table = print_rule_input(ip)
            output_table = print_rule_output(ip)
    print(print_closure())

if __name__ == "__main__":
    # Unbuffer output (this ensures the output is in the correct order)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    tee = subprocess.Popen(["tee", "iptables.txt"], stdin=subprocess.PIPE)
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())
    #run the shit
    main(sys.argv)
