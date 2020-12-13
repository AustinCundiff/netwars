import socket
from threading import Thread
import parser
import sys
import argparse
import re
import select

class Proxy2Server(Thread):

    def __init__(self,host,port,deny):
        super(Proxy2Server,self).__init__()
        self.NextServer = None
        self.NextServerthread = None
        self.port = port
        self.host = host
	self.deny = deny
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.connect((host,port))
	self.exit = False
    
    def run(self):
        while True:
	    if self.exit:
		return	
	    try:
        	data = self.server.recv(4096)
	    except socket.timeout:
		continue
            if data:
                try:
                    reload(parser)
                    allow = parser.parse(data,self.port,'server',self.host)
		    if allow:
                    	self.NextServer.sendall(data)
		    else:
			self.NextServer.sendall(self.deny)
			self.NextServer.close()
			self.server.close()
			self.NextServerthread.exit = True
			return	
                except Exception as e:
                    print('server[{}]'.format(self.port),e)
		    return


class Client2Proxy(Thread):

    def __init__(self,host,port,deny):
        super(Client2Proxy,self).__init__()
        self.server = None
        self.serverthread = None
        self.port = port
        self.host = host
	self.deny = deny
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((host,port))
        sock.listen(1)
        self.NextServer,self.addr = sock.accept()
	self.exit = False
    
    def run(self):
	self.NextServer.settimeout(0.5)
        while True:
		if self.exit:
			return

		try:
        		data = self.NextServer.recv(4096)
		except socket.timeout:
			continue
		if data:
			try:
				reload(parser)
		        	allow = parser.parse(data,self.port,'client',self.addr[0])
				if allow:
					if 'accept-encoding' in data.lower():
						data = re.sub(r'accept-encoding: [a-zA-Z\,\; ]*','Accept-Encoding: identity',data,flags=re.IGNORECASE)
			               	self.server.sendall(data)
			    	else:
					self.NextServer.sendall(self.deny)
					self.server.close()
					self.NextServer.close()
					self.serverthread.exit = True
					return	
			except Exception as e:
				print('client[{}]'.format(self.port),e)
				return

class Proxy(Thread):
    def __init__(self,from_host,bind_port,to_host,port):
        super(Proxy,self).__init__()
        self.from_host = from_host
        self.to_host=to_host
        self.bind_port = bind_port
        self.port = port
	self.deny = parser.DENY_MESSAGE

    def run(self):
        while True:
            #print("[proxy({})] setting up".format(self.port))
            self.c2p = Client2Proxy(self.from_host,self.bind_port,self.deny)
            self.p2s = Proxy2Server(self.to_host,self.port,self.deny)
            #print("[proxy({})] connection established".format(self.port))
	    self.c2p.serverthread = self.p2s
            self.c2p.server=self.p2s.server
            self.p2s.NextServerthread=self.c2p
            self.p2s.NextServer=self.c2p.NextServer

            self.c2p.start()
            self.p2s.start()

if __name__ == '__main__':
	argparser = argparse.ArgumentParser("Attempts to proxy a connection")
	argparser.add_argument("-b","--bind",help="IP to bind to",required=True,type=str)
	argparser.add_argument("-l","--listen",help="Port to listen on",required=True,type=int)
	argparser.add_argument("-r","--remote",help="Destination IP",required=True,type=str)
	argparser.add_argument("-p","--port",help="Destination port",required=True,type=int)
	args = argparser.parse_args()
	
	master_server = Proxy(args.bind,args.listen,args.remote,args.port)
	master_server.start()

	while True:
	    cmd = raw_input("> ")
	    if cmd=='q':
        	sys.exit(0)
