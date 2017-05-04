import time
import os
import threading
import subprocess
import binascii, sys, stat
import re
import socket
import json
from SocketServer import *
from threading import Thread, Timer
from time import sleep

portbase=8000
Nodes=[]
Nodes.append('Test')
buffersize=2048

class Node(Thread):
	def __init__(self, num, neighbours, costs, total):
		Thread.__init__(self)
		self.fTable=[100000000 for x in range(total)]
		self.fTable[num]=0
		self.neighbours=neighbours
		self.costs=costs
		self.num=num
		self.port=portbase+num
		self.u=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.u.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.u.bind(('', self.port))

	def run(self):
		while True:
			msg,addr=self.u.recvfrom(buffersize)
			data=json.loads(msg)
			#print data
			hostname, sport = addr
			#print str(self.num) + ' received from ' + str(sport)
			#print str(data[1])+' hello'
			sno=int(sport)-portbase
			snoi=self.neighbours.index(sno)
			k=len(data)
			sc=self.costs[snoi]
			#print k
			for j in range(k):
				if sc+data[j]<self.fTable[j]:
					self.fTable[j]=sc+data[j]


	def printfTable(self):
		return self.fTable




	def sendtable(self):
		data=json.dumps(self.fTable)
		#print self.neighbours
		for i in self.neighbours:
			self.st(data, i)

	def st(self, data, to):
		addr=('',portbase+to)
		#sleep(1)
		self.u.sendto(data, addr)






a, b = 6, 6;
adjm = [[0 for x in range(a)] for y in range(b)] 
wm = [[1000000 for x in range(a)] for y in range(b)] 
fp=open('graph.txt', 'r')
graph=fp.read()
graph=graph.split('\n')
#print graph
v=int(graph[0])
c=len(graph)-1
#print v
for i in range(1,c):
	d=graph[i].split()
	dn=d[0]
	neighbours=[]
	costs=[]
	for j in range(int(dn)):
		neighbours.append(int(d[(2*j)+1]))
		costs.append(int(d[(2*j)+2]))
	#print neighbours
	#print costs
	newNode=Node(i, neighbours, costs, c)
	Nodes.append(newNode)
	newNode.start()

def BellUpdate():
	global Nodes
	#for i in range(v-1):
	#	for j in range(v):
	#		Nodes[j].sendtable()
	for i in range(c):
		for j in range(1,c):
			#print j
			Nodes[j].sendtable()
	#Nodes[1].sendtable()
	temp=str(v)+"\n"
	for j in range(1,c):
		a=Nodes[j].printfTable()
		temp=temp+str(v-1)
		for i in range(1,len(a)):
			if i==j:
				continue
			temp=temp+' '+str(i)+' '+str(a[i])
		temp=temp+'\n'
	print temp
	fp = open('output.txt', 'w')
	fp.write(temp)
	fp.close()
	t=Timer(30, BellUpdate)
	t.start()

BellUpdate()




