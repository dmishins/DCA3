import socket   #for sockets
import sys  #for exit
import struct
import time
import datetime
import re
import os, errno
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import argparse
import warnings
from scp import SCPClient
import os
import re
import errno
import time
import datetime
from ROOT import TFile, TTree
from array import array
from math import floor, ceil

#print args
def signed(val):
	if val > 2048:
		return val - 4096
	return val

class event:
	headerlen = 32
	maxlen = 0
	def __init__(self, data):
		self.headerraw = None
		self.ch1raw = None
		self.ch2raw = None
		self.ch3raw = None
		self.ch4raw = None

		self.header = []
		self.ch1 = []
		self.ch2 = []
		self.ch3 = []
		self.ch4 = []

		self.extract(data)
		if self.ch1raw == None or self.ch2raw == None or self.ch3raw == None or self.ch4raw == None or self.headerraw == None:
			print "Bad Data"
			print self.headerraw

			print self.ch1raw
			print self.ch2raw
			print self.ch3raw
			print self.ch4raw


			#exit()
		else:
			self.process()
			self.ch1maxadc = max(self.ch1)
			self.ch2maxadc = max(self.ch2)
			self.ch3maxadc = max(self.ch3)
			self.ch4maxadc = max(self.ch4)
			self.ch1maxidx = self.ch1.index(max(self.ch1))
			self.ch2maxidx = self.ch2.index(max(self.ch2))
			self.ch3maxidx = self.ch3.index(max(self.ch3))
			self.ch4maxidx = self.ch4.index(max(self.ch4))
#                        #print self.ch4[max(0, self.ch4maxidx-3):self.ch4maxidx]
#                        #print self.ch4maxidx
#                        self.ch1mymax = self.ch1maxadc - min(self.ch1[max(0, self.ch1maxidx-3):self.ch1maxidx+1])
#                        self.ch2mymax = self.ch2maxadc - min(self.ch2[max(0, self.ch2maxidx-3):self.ch2maxidx+1])
#                        self.ch3mymax = self.ch3maxadc - min(self.ch3[max(0, self.ch3maxidx-3):self.ch3maxidx+1])
#                        self.ch4mymax = self.ch4maxadc - min(self.ch4[max(0, self.ch4maxidx-3):self.ch4maxidx+1])
#                        self.integrate()

		#else:
			#print "ERROR. ", self.ch1raw, self.ch2raw, self.ch3raw, self.ch4raw


	def extract(self, data):
		self.headerraw = data[:event.headerlen]
		self.eventlength = int(self.headerraw[20:24], 16) - 1
		if event.maxlen < self.eventlength:
			event.maxlen = self.eventlength
		ptr = event.headerlen+4
		self.ch1raw = data[ptr:ptr + self.eventlength*4]
		ptr += ((self.eventlength * 4)+4)
		self.ch2raw = data[ptr:ptr + self.eventlength*4]
		ptr += ((self.eventlength * 4)+4)
		self.ch3raw = data[ptr:ptr + self.eventlength*4]
		ptr += ((self.eventlength * 4)+4)
		self.ch4raw = data[ptr:ptr + self.eventlength*4]

	def process(self):
		self.ch1 = [signed(int(self.ch1raw[i:i+4],16)) for i in range(0, len(self.ch1raw), 4)]
		self.ch2 = [signed(int(self.ch2raw[i:i+4],16)) for i in range(0, len(self.ch2raw), 4)]
		self.ch3 = [signed(int(self.ch3raw[i:i+4],16)) for i in range(0, len(self.ch3raw), 4)]
		self.ch4 = [signed(int(self.ch4raw[i:i+4],16)) for i in range(0, len(self.ch4raw), 4)]
		#print self.headerraw
		try:
			self.wc = int(self.headerraw[:4],16)
			self.ts = int(self.headerraw[4:12],16)
			self.tc = int(self.headerraw[12:20],16)
			self.sp = int(self.headerraw[20:24],16)
			self.tt = int(self.headerraw[24:28],16)
			self.es = int(self.headerraw[28:32],16)
		except:
			print "bad event"

	def integrate(self):
		self.ch1area = np.trapz(self.ch1[self.ch1maxidx-2:self.ch1maxidx+2])
		self.ch2area = np.trapz(self.ch2[self.ch2maxidx-2:self.ch2maxidx+2])
		self.ch3area = np.trapz(self.ch3[self.ch3maxidx-2:self.ch3maxidx+2])
		self.ch4area = np.trapz(self.ch4[self.ch4maxidx-2:self.ch4maxidx+2])



s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.settimeout(5)
s.connect(("192.168.0.19", 5002))
time.sleep(1)
s.send("wr 308 1" + "\r")
s.recv(1024)
time.sleep(.5)
while True:
	print "Take Data (wr 303 300)"
	s.send('wr 303 300\r')
	s.recv(1024)

	while True:
		#print "Checking if spill done"
		s.send('rd 303\r')
		time.sleep(.01)
		rd303 = re.search(r'[0-9A-F]+', s.recv(1024)).group() 
		if rd303 == "0000":
			break
		time.sleep(.1)
	s.settimeout(1)
	print "done"
	#try:
	#	s.recv(1024)
	#except:
	#	print "Ready"
	s.send('rdb\r\n')
	#s.recv(1024)
	buf = ""
	for i in range(1000):
		try:
			buf += s.recv(1024)
		except socket.timeout:
			print "Readout Attempts: ", i-1
			break

	events = []

	dump = "".join(buf).encode('hex_codec')[:]
	print "Buffer len: ", len(dump)
	#events = [x for x in re.split('(03c8)', joinedall) if x]
	ptr = 34
	spillheader = dump[:32]
	print "HEADER: ", spillheader
	tgrexp =  int(spillheader[8:16],16)
	trgrcv = 0
	i = 0
	ch = "ch1"
	while trgrcv < tgrexp:
		if not dump[ptr:ptr+32]:
			print "ERROR at event ", trgrcv, " at position: ", ptr
			print "Dump: ", dump[ptr:ptr+32]
			trgrcv += 1
			continue

		#print dump[ptr:ptr+32], trgrcv
		eventsize = int(dump[ptr:ptr+4],16)*4

		#print eventsize, ptr, i 
	            #if eventsize != int("03c8",16)*4:
		#	print "ERR: Event size wrong: ", eventsize, " for event: " + str(trgrcv) + " at ptr: " + str(ptr)
		#	print "Making eventsize 03c8 to mitigate readout bug"
		#	eventsize = int("03c8",16)*4

		#print eventsize
		#print dump[ptr:ptr+eventsize] + "\n\n"
		events.append(event(dump[ptr:ptr+eventsize]))
		ptr += eventsize
		trgrcv += 1
		plt.figure("Waveform")
		#noisy = [0, 6, 9, 11,18]
	plt.clf()
	#plt.figure("Waveform")

	plt.ion()
	plt.show()
	for i, indiv_event in enumerate(events[:]): #[events[x] for x in noisy]:
	#        if 1==1: # getattr(indiv_event, ch+"maxadc") > 20 and getattr(indiv_event, ch+"maxadc") < 30:
		#plt.clf()
		plt.plot(getattr(indiv_event, "ch1"), label=("ch1"+str(i)))
		plt.ylim((-15,5))
		plt.title("ch1")
		plt.xlabel('ticks')
		plt.ylabel('ADC')
		plt.draw()
		#plt.pause(.01)
		#plt.show(block=False)
		#print i
	plt.show()
	plt.draw()
	plt.pause(.0001)





s.close()
 
