import socket   #for sockets
import sys  #for exit
import struct
import time
import datetime
import re
import os, errno
import argparse

parser = argparse.ArgumentParser(description='Take Data from DAPHNE board')
parser.add_argument('filename', nargs='?',
                    help='the filename to write to in the DATA/{DATE} directory.')
parser.add_argument('--daphne_port', action='store', default="5000",
                    help='path to daphne board', type=int)
parser.add_argument('--daphne_addr', action='store', default="192.168.0.19",
                    help='path to daphne board')
parser.add_argument('-f', action='store_true',
                    help='use the relative path, not DATA/{DATE}')
parser.add_argument('--overwrite', action='store_true',
                    help='allow overwriting filename')
parser.add_argument('--command', 
                    help='run command on board, then take data')
parser.add_argument('--command_stop', action='store_true',
                    help='run command on board, then stop')
parser.add_argument('--spill_length', action='store',
                    help='sets the spill length. HEX')
parser.add_argument('--get_current', action='store',
                    help='gets the current for a given port')

args = parser.parse_args()
#print args
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.settimeout(10)
s.connect((args.daphne_addr, args.daphne_port))

if args.get_current != None:
	addr = int(args.get_current)
	indx_lst = ['0','4','8','C']
	board_indx = addr//16
	board = f'{board_lst[board_indx]}20'
	remainder = addr%16
	port = hex(remainder)[2:]
	port_indx = int(port)//4
	port_num = int(port)%4

	for x in range(3):
		if x == board_indx:
			continue
		s.send(f'wr {board_lst[x]}20 0 \r')
		print s.recv(1024)
		time.sleep(.5)
	
	if board_indx == 0:
		s.send('mux 0 \r')
		print s.recv(1024)
		time.sleep(.5)
		s.send(f'wr 20 1{port} \r')
		print s.recv(1024)
		time.sleep(.5)

	else:
		s.send(f'mux {board_indx} \r')
		print s.recv(1024)
		time.sleep(.5)
		s.send(f'wr {board} 1{indx_lst[port_indx]} \r')
		s.send(f'wr 20 0{port_num} \r')
		print s.recv(1024)
		time.sleep(.5)

	s.send(f'a0 1 \r')
	print s.recv(1024)
	time.sleep(.5)


if args.spill_length != None:
	s.send("wr 308 " + args.spill_length + "\r")
	print s.recv(1024)
	time.sleep(.5)
	s.send("rd 308 \r")
	print s.recv(1024)
	time.sleep(2)

if args.command != None:
	s.send(args.command + "\r")
	print s.recv(4096)
if args.command_stop:
	print "Command Finished. Exiting."
	exit(0)
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

if args.f == False:
	rel_path = "DAPHNE/DATA/{}/{}.bin".format(date, args.filename)
	filepath = os.path.expanduser("~/" + rel_path)
	directory = os.path.dirname(filepath)
	try:
	    os.makedirs(directory)
	except OSError as e:
	    if e.errno != errno.EEXIST:
		raise
else:
	filepath = args.filename
if os.path.isfile(filepath) and not args.overwrite:
	print "File Already exists. Exiting. use --overwrite to ignore"
	exit(1)


file = open(filepath,"w") 

st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
file.write(str(ts))
file.write('\n')
RD_LEN = 1024

#print "filepath: " + filepath

print "Take Data (wr 303 300)"
s.send('wr 303 300\r')
s.recv(1024)
if args.spill_length:
	print "Wait "+str(args.spill_length)+" S"
	time.sleep(float(args.spill_length))
else:
	print "Wait 2 S"
	time.sleep(2)
s.send('rd 67\r')
time.sleep(.25)
print "READ 67: ", re.search(r'[0-9A-F]+', s.recv(1024)).group()
count = 0
while True:
	print "Checking if spill done"
	s.send('rd 303\r')
	time.sleep(.1)
	rd303 = re.search(r'[0-9A-F]+', s.recv(1024)).group() 
	print "Spill Reg value:", rd303
	time.sleep(.1)
	s.send('rd 67\r')
	if rd303 == "0000":
		print "Spill Done. 67: ", re.search(r'[0-9A-F]+', s.recv(1024)).group()
		break
	count += 1
	print "Spill Not Done. 67: ", re.search(r'[0-9A-F]+', s.recv(1024)).group(), " count is:", count
	time.sleep(1)
s.settimeout(1)
try:
	s.recv(1024)
except:
	print "Ready"
s.send('rdb\r\n')
#s.recv(1024)
for i in range(100000):
	try:
		buf = s.recv(RD_LEN)
	except socket.timeout:
		print "Readout Attempts: ", i-1
		break
	file.write(buf)

s.close()
 
print "filepath: " + filepath
