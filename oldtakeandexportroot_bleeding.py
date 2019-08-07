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
with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	import paramiko

parser = argparse.ArgumentParser(description='Take and process data from DAPHNE board')
parser.add_argument('filename', nargs='?',
                    help='the filename to write to in the DATA/{DATE} directory.')
parser.add_argument('-d', action='store_true',
                    help='use  DATA/{DATE}.  instead of relative path')
parser.add_argument('--overwrite', action='store_true',
                    help='allow overwriting filename.')
parser.add_argument('--super', action='store_true',
                    help='superimpose plots')
parser.add_argument('--command', 
                    help='run command on board, then take data')
parser.add_argument('--command_stop', action = 'store_true',
                    help='run command on board, then stop')
parser.add_argument('--ignore_timestamp', action = 'store_true',
                    help='ignore timestamp')
parser.add_argument('--root', action = 'store',
                    help='output root ttree file')
parser.add_argument('--directory', action = 'store_true',
                    help='directory of bin files to process')
parser.add_argument('--feedthrough', metavar = 'FLAG',
                    help='Feed flag through to server script')
parser.add_argument('--server_script_location', default="DAPHNE/takeBinaryData.py")
parser.add_argument('-r', action='store_true',
                    help='connect to server and take remote data. DO not use local file')
parser.add_argument('-p', action='store', nargs = '*',
                    help='plot channels')
parser.add_argument('--fft', action='store', nargs = '*',
                    help='plot fft channels')
parser.add_argument('--hist', action='store', nargs = '*',
                    help='plot max adc hist for channels')
parser.add_argument('--ahist', action='store', nargs = '*',
                    help='plot area  hist for channels')
parser.add_argument('--pltnum', action='store', type=int,
                    help='number of signals to plt.')
parser.add_argument('--filter', action='store', nargs = '*',
                    help='filter based on following channels.  Currently filter settings must be changed by editing code')
parser.add_argument('-s', dest='server', action='store',
                	default="protodune-daq01.fnal.gov",
                    help='The server to connect to. Default: protodune-daq01.fnal.gov')
parser.add_argument('--spill_length', action='store',
                    help='sets the spill length. HEX')
parser.add_argument('-u', dest='username', action='store',
                	default="dunepdt",
                    help='The server to connect to. Default: dunepdt')

args = parser.parse_args()

#print args
#exit()
if args.r == True:
	localpath = takeremotedata()
else:
	localpath = args.filename
	if args.d == True:
		ts = time.time()
		date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

		localpath = str("DATA/"+date+"/"+args.filename+".bin")

print localpath


def takeremotedata():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys() 
		ssh.connect(args.server, username=args.username, gss_auth = True )
	ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python -u "+ args.server_script_location +
		(" " + args.feedthrough if args.feedthrough else "") + (" " + ("--command \"" + args.command) +
		 "\"" if args.command else "")+(" --command_stop" if args.command_stop else "")+ (" " + (args.filename)
		  if args.filename else "")+(" --overwrite" if args.overwrite else "")+((" --spill_length " + args.spill_length) if args.spill_length else ""))
	while True:
		outline = ssh_stdout.readline()
		if not outline:
			break
		if outline.startswith("filepath"):
			filepath = outline.split(" ")[-1].rstrip("\n\r")
		print outline

	err_read = ssh_stderr.read()
	if err_read:
		print "SSH: STDerr IS ", err_read 
	if args.command_stop:
		exit()
	#filepath = "DAPHNE/binarytest"  #Manually override path
	if args.f == False:
		localpath = "/".join(filepath.split("/")[-3:]).encode("utf-8")
	else:
		localpath = args.f
	print localpath
	scp = SCPClient(ssh.get_transport())
	directory = os.path.dirname(localpath)
	try:
	    os.makedirs(directory)
	except OSError as e:
	    if e.errno != errno.EEXIST:
	        raise


	scp.get(filepath, localpath)
	return localpath



def signed(val):
	if val > 2048:
		return val - 4096
	return val

def plotchannel(events, ch, super=False):
	plt.figure("Waveform")
	#noisy = [0, 6, 9, 11,18]
	for i, indiv_event in enumerate(events[:args.pltnum]): #[events[x] for x in noisy]:
            if 1==1: # getattr(indiv_event, ch+"maxadc") > 20 and getattr(indiv_event, ch+"maxadc") < 30:
		plt.plot(getattr(indiv_event, ch), label=(ch+str(i)))
		plt.title(ch)
		plt.xlabel('ticks')
		plt.ylabel('ADC')
		if super == False:
		    plt.title(ch + " Event: " + str(i+1) )
		    plt.show()
		    #print getattr(indiv_event, ch)
		else:
		    plt.show(block=False)
	#plt.draw()

def histchannel(events, ch):
	plt.figure("MAX ADC Histogram")
	maxadcvals = []
	#noisy = [0, 6, 9, 11,18]
	for i, indiv_event in enumerate(events[:args.pltnum]): #[events[x] for x in noisy]:
		maxadcvals.append(getattr(indiv_event, ch+"maxadc"))
	plt.hist(maxadcvals, bins=50)#range(min(maxadcvals), max(maxadcvals) + 1, 1))
	plt.xlabel('MAX ADC value in event')
	plt.ylabel('# Of events')
	plt.title("MAX ADC Histogram")
	plt.yscale('log')
        plt.show(block=False)
	#plt.draw()

def ahistchannel(events, ch):
	plt.figure("Area Histogram")
	areavals = []
	#noisy = [0, 6, 9, 11,18]
	for i, indiv_event in enumerate(events[:args.pltnum]): #[events[x] for x in noisy]:
		areavals.append(getattr(indiv_event, ch+"area"))
	plt.hist(areavals,  bins=50)#range(int(floor(min(areavals))), int(ceil(max(areavals))) + 1, 1))

	plt.xlabel('Area around max adc value in event')
	plt.ylabel('ADC')
	plt.title("Area Around Max Histogram")
        plt.yscale('log')
	plt.show(block=False)



def fftchannel(events, ch, super=False):
	f_s = 1/12.55e-9

	plt.figure("FFT")
	#noisy = [0, 6, 9, 11,18]  #Use this and the following comment to manually select which events to plot fft
	totalfft = np.zeros(239, dtype = np.complex128)
	for i, indiv_event in enumerate(events[:args.pltnum]): #[events[x] for x in noisy]:
		evchdata = getattr(indiv_event, ch)
		eventfft = np.fft.fft(evchdata)
		freqs = np.fft.fftfreq(len(evchdata)) * f_s
		if np.shape(eventfft) == (239,):
			totalfft = totalfft + abs(eventfft)
		#plt.plot(abs(freqs/1e6), abs(eventfft))
		#plt.xlabel('Frequency (MHz)')
		#plt.xlim(0,f_s//1e6//2)
                #plt.title(ch + " FFT")


		#plt.title(ch)
		if super == False:
			plt.title(ch + " Event: " + str(i+1) )
			plt.show()
	plt.plot(abs(freqs/1e6), abs(totalfft))
	plt.show(block=False)

def filter(events, ch):
	filteredevents = []
	for i, indiv_event in enumerate(events): #[events[x] for x in noisy]:
		fft = np.fft.fft(getattr(indiv_event, ch))
		if max(abs(fft[8:11]))< 275:
			filteredevents.append(indiv_event)
	return filteredevents


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
			self.integrate()

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


def process_file(localpath):
	f = open(localpath, "rb")
	remote_timestamp = f.readline()
	if not args.ignore_timestamp:
		st = datetime.datetime.fromtimestamp(float(remote_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
		print "TIMESTAMP: ", st

	lines = f.readlines()

	dump = "".join(lines).encode('hex_codec')[:]
	print "Buffer len: ", len(dump)
	#events = [x for x in re.split('(03c8)', joinedall) if x]
	ptr = 34
	spillheader = dump[:32]
	print "HEADER: ", spillheader
	tgrexp =  int(spillheader[8:16],16)
	trgrcv = 0
	i = 0
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


events = []
if args.directory:
	for filename in os.listdir(localpath):
		print filename
		process_file(localpath + "/" + filename)
else:
	process_file(localpath)

if args.filter:
	for channel in args.filter:
		events = filter(events, channel)


if events:
	print "Length of Event[0].ch1: ", len(events[0].ch1)
	print "Number of Events Processed: ", len(events)

	avgadcvals = np.zeros(len(events[0].ch1))
	goodevents = []

	if args.root:
		f = TFile( args.root, 'recreate' )
		t = TTree( 't1', 'adc data' )
		 
		maxn = event.maxlen
		print maxn
		d1 = array( 'i', maxn*[ 0 ] )
		d2 = array( 'i', maxn*[ 0 ] )
		d3 = array( 'i', maxn*[ 0 ] )
		d4 = array( 'i', maxn*[ 0 ] )

		t.Branch( 'ch1', d1, 'ch1['+str(maxn)+']/I' )
		t.Branch( 'ch2', d2, 'ch2['+str(maxn)+']/I' )
		t.Branch( 'ch3', d3, 'ch3['+str(maxn)+']/I' )
		t.Branch( 'ch4', d4, 'ch4['+str(maxn)+']/I' )

		for event in events:
			for j in range(event.eventlength):
				d1[j] = event.ch1[j]
				#print d1[j]
				d2[j] = event.ch2[j]
				d3[j] = event.ch3[j]
				d4[j] = event.ch4[j]
			#print d1
			t.Fill()
		#t.Print()
		#t.Show(0)
		#t.Show(1)
		#t.Show(2)
		#t.Show(3)
		#t.Scan("*")

		f.Write()
		f.Close()
		#if peakidx > 64 and peakidx < 72 and maxval > 0 and maxval < 20:
		## if peakidx > 64 and peakidx < 72 and maxval > 10:	
		#	goodevents.append(event)

	# plt.figure()
	# plt.plot(avgadcvals, label='X ARAPUCA (average waveform)')
	# plt.title('')
	# plt.xlabel('ticks (1 tick = 12.55 ns)')
	# plt.ylabel('ADC')
	# # plt.legend()
	# plt.xlim([0,240])
	# plt.show()


	#maxadc = np.asarray(maxadc)

	#plt.figure()
	#bins = np.linspace(-100, 500, 601)
	#plt.hist(maxadc, bins)
	#plt.title('max ADC')
	#plt.xlabel('max ADC')
	#plt.ylabel('counts')
	#plt.xlim([-20,200])
	## plt.legend()
	## plt.yscale('log')
	#plt.show()

	# print len(goodevents)

	# # scan through individual events

	if args.p:
		for channel in args.p:
			plotchannel(events, channel, super=args.super)

	if args.hist:
		for channel in args.hist:
			histchannel(events, channel)

	if args.ahist:
		for channel in args.ahist:
			ahistchannel(events, channel)


	if args.fft:
		for channel in args.fft:
			fftchannel(events, channel, super=args.super)
	plt.show()



else:
	print "Events Empty"
