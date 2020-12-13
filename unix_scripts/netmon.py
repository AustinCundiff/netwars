#!/usr/bin/python
import subprocess
import os
from threading import Thread
import time
import hashlib

WHITELIST = ['myConnection']

menu = "[1] Add to the whitelist\n[2] Print the whitelist\n[3] Remove from the whitelist\n[4] Set maximum connection time\n[5] Exit\n> "

class MainLoop(Thread):
	def __init__(self):
		super(MainLoop,self).__init__()
		self.exit = False
		self.connections = {}
		self.max_time = 30

	def killPID(self,pid):
		#print("killing {}".format(pid))
		try:
			subprocess.check_output("kill -9 {} 2>/dev/null".format(pid),shell=True)
		except:
			pass
		
	def getNetstat(self):
		temp_entries = {}
		procs	= subprocess.check_output("netstat -untap 2>/dev/null | grep ESTAB",shell=True)
		splits	= procs.decode('utf-8').split("\n")
		for i in splits:
			if any(good in i for good in WHITELIST):
				continue
			try:
				last_args = ' '.join(i.split()[6:]).split('/')
				pid  = last_args[0]
				if pid.isdigit():
					md5sum = hashlib.md5(i.encode()).hexdigest()
					temp_entries[md5sum] = [time.time(),time.time(),pid]
				else:
					continue
			except Exception as e:
				print("[Error] {}".format(e))
				pass
		self.updateTracker(temp_entries)

	def updateTracker(self,new_list):
		kill_list = []
		for i in new_list.keys():
			if i in self.connections.keys():
				self.connections[i][1]  = new_list[i][1]
			else:
				self.connections[i] = [new_list[i][0],new_list[i][1],new_list[i][2]]

		removed_list = []	
		for i in self.connections.keys():
			if i not in new_list.keys():
				removed_list.append(i)

			if self.connections[i][1] - self.connections[i][0] >= self.max_time:
				kill_list.append([i,self.connections[i][2]])
		for i in removed_list:
			self.connections.pop(i)

		for i in kill_list:
			self.killPID(i[1])
			self.connections.pop(i[0])

	def run(self):
		while True:
			if self.exit==True:
				break
			self.getNetstat()
			time.sleep(2)


def printList():
	print("\n"+"#"*30)
	for x,y in enumerate(WHITELIST):
		print("[{}]\t{}".format(x,y))
	print("\n"+"#"*30+"\n")

if __name__ == '__main__':
	x = MainLoop()
	x.start()
	
	while True:
		val = input(menu)
		if val == '1':
			WHITELIST.append(input("New whitelist value: "))
			printList()
		elif val == '2':
			printList()
		elif val == '3':
			printList()
			idx = input("Which whitelist value would you like to remove: ")
			if idx.isdigit():
				try:
					WHITELIST.pop(int(idx))
					print("#"*10+" New List "+"#"*10)
					printList()
				except Exception as e:
					print("Please pick a valid index")
			else:
				print("Please use index values")
		elif val == '4':
			timer = input("Maximum connection time (in seconds): ")
			if timer.isdigit():
				x.max_time=int(timer)
			else:
				print("Please provide a valid integer")
		elif val == '5':
			x.exit = True
			break
		
