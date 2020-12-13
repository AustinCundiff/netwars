INPUT_BLACKLIST = ['/bin/sh','/bin/bash','../','%2e%2e',\
                   'a'*200,'or 1=1',"or '1'='1","information_schema"]

OUTPUT_BLACKLIST = []

IP_WHITELIST=[]
IP_BLACKLIST=[]

DENY_MESSAGE = '''315th Dragons Own The Net

This exploit is no longer allowed.
'''

################# Do not edit below here ###############3


INPUT_BLACKLIST = list([x.lower() for x in INPUT_BLACKLIST])
OUTPUT_BLACKLIST = list([x.lower() for x in OUTPUT_BLACKLIST])


def parse(data,port,origin,addr=''):
        #print("[{}:({})] {}\n".format(origin,port,data.encode('hex')))
	data = data.lower()
	if origin == 'client':
		return parse_input(data,addr)
	else:
		return parse_output(data,addr)

def parse_input(data,addr):
	
	# Check for explicitly blocked or allowed client IPs
	if addr in IP_WHITELIST:
		return True
	if addr in IP_BLACKLIST:
		return False

	# Check for bad input (Looking for things that look like exploits here)
	if any(bad in data for bad in INPUT_BLACKLIST):
		return False		
	return True

def parse_output(data,addr):

	# Check for explicitly blocked or allowed client IPs - (its likely that blocked isn't necessary here)	
	if addr in IP_WHITELIST:
		return True
	if addr in IP_BLACKLIST:
		return False

	# Check for bad output (Looking for things that look like flags here)
	if any(bad in data for bad in OUTPUT_BLACKLIST):
		return False		
	return True
