import socket  # for sockets
import sys  # for exit
import struct
import time
import datetime
import re
import os
import errno
import argparse

parser = argparse.ArgumentParser(description='Take Data from DAPHNE board')
parser.add_argument('filename', nargs='?',
                    help='the filename to write to in the DATA/{DATE} directory.')
parser.add_argument('--daphne_port', action='store', default="5000",
                    help='path to daphne board', type=int)
parser.add_argument('--daphne_addr', action='store', default="192.168.0.19",
                    help='path to daphne board')
parser.add_argument('-f', action='store_true',
                    help='use the DATA/{DATE}, not relative path')
parser.add_argument('--overwrite', action='store_true',
                    help='allow overwriting filename')
parser.add_argument('--command',
                    help='run command on board, then take data')
parser.add_argument('--command_stop', action='store_true',
                    help='run command on board, then stop')
parser.add_argument('--debug', action='store_true',
                    help='prints extra debug info')
parser.add_argument('--setup', action='store_true',
                    help='runs board setup')
parser.add_argument('--spill_length', action='store',
                    help='sets the spill length. HEX')
parser.add_argument('--get_current', action='store',
                    help='gets the current for a given chanel')
parser.add_argument('--set_voltage', action='store',
                    help='set voltage (DANGER)', type=float)
parser.add_argument('--read_voltage', action='store_true',
                    help='read voltage')
parser.add_argument('--v_ch', action='store',
                    help='the register to write voltage. use -1 for all')
parser.add_argument('--force_voltage', action='store_true',
                    help='override 62v limit')
args = parser.parse_args()
# print args
class connection:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(10)
    s.connect((args.daphne_addr, args.daphne_port))
    def recv(self, n):
        return self.s.recv(n)
    def send(self, val):
        #print(self, val)
        if (isinstance(val, str)):
             return self.s.send(val.encode())
        else:
            return self.s.send(val)
    def settimeout(self, n):
        self.s.settimeout(n)
    def close(self):
        self.s.close()

s = connection()
def rd_board(debug):
    rd = s.recv(1024)
    if debug:
        print("\n".join(rd.decode().splitlines()))
    return rd

def read_current_channel(channel, debug):
    indx_lst = ['0', '4', '8', 'C']
    board_indx = channel//16
    board = '{}20'.format(indx_lst[board_indx])
    remainder = channel % 16
    port = hex(remainder)[2:]
    port_indx = int(remainder)//4
    port_num = int(remainder) % 4

    for x in range(4):
        if x == board_indx:
            continue
        s.send('wr {}20 0 \r'.format(indx_lst[x]))  # Turn off all other muxes
        rd_board(debug)

    if board_indx == 0:
        s.send('mux 0 \r')
        rd_board(debug)
        # time.sleep(.5)
        s.send('wr 20 1{} \r'.format(port))
        rd_board(debug)

    else:
        s.send('mux {} \r'.format(board_indx))
        rd_board(debug)
        time.sleep(.1)
        s.send('wr {} 1{} \r'.format(board, indx_lst[port_indx]))
        rd_board(debug)
        time.sleep(.1)
        s.send('wr 20 0{} \r'.format(port_num))
        rd_board(debug)
        time.sleep(.1)

    s.send('gain 8 \r')
    rd_board(debug)
    s.send('a0 1 \r')
    #rd_board(debug)  # get back echo?
    readval = rd_board(debug).splitlines()[0]
    count = 0
    print(readval)
    while (readval == b">" and count < 3):
        print("Bad read(ch, val): {}, {}".format(channel, readval))
        s.send('a0 5 \r')
        # rd_board(debug)  # get back echo?
        readval = rd_board(debug)#.splitlines()[0]
        print("after: {} ".format(readval))
        time.sleep(.4)
        count += 1
    return readval.decode()

if args.setup == True:
    setupfile = open("setup.ds")
    setuplines = setupfile.read().splitlines()
    for line in setuplines:
        s.send((line.split("#")[0] + "\r").encode())
        rd_board(args.debug)
        #print(line.split("#")[0] + "\r")

if args.set_voltage != None:
    if args.set_voltage > 62 and not args.force_voltage:
        print ("Voltage over 62 is restricted.  use --force_voltage to override")
        exit()
    V = int(args.set_voltage / 5.38 * 256)
    hex_V = '{:02x}'.format(V)
    print("Setting voltage hex code to: " + hex_V)
    if args.v_ch == "-1":
        indx_lst = ['0', '4', '8', 'C']
        for fpga in indx_lst:
            s.send('wr {}44 {} \r'.format(fpga, hex_V))
            rd_board(args.debug)
            s.send('wr {}45 {} \r'.format(fpga, hex_V))
            rd_board(args.debug)
    elif args.v_ch:
        s.send('wr {} {} \r'.format(args.v_ch, hex_V))
        rd_board(args.debug)
    else:
        print("Choose a channel. Voltage setting failed")

if args.read_voltage == True:
    s.send("adc \r")
    time.sleep(.5)
    rd_board(1)

if args.get_current != None:
    addr = int(args.get_current)
    debug = args.debug
    if addr == -1:
        if os.path.isfile(args.filename + ".a0") and not args.overwrite:
            print("File Already exists. Exiting. use --overwrite to ignore")
            exit(1)
        file = open(args.filename + ".a0", "w")

        for ch in range(64):
            file.write(str(ch) + ": " + read_current_channel(ch, debug) + "\n")
    else:
        print(read_current_channel(addr, debug))
    for x in range(4):
        indx_lst = ['0', '4', '8', 'C']
        s.send('wr {}20 0 \r'.format(indx_lst[x]))
        rd_board(debug)
        time.sleep(.5)


if args.spill_length != None:
    s.send("wr 308 " + args.spill_length + "\r")
    print(s.recv(1024))
    time.sleep(.5)
    s.send("rd 308 \r")
    print(s.recv(1024))
    time.sleep(2)

if args.command != None:
    s.send(args.command + "\r")
    print(s.recv(4096))
if args.command_stop:
    print("Command Finished. Exiting.")
    exit(0)
ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

if args.f == True:
    rel_path = "DAPHNE/DATA/{}/{}.bin".format(date, args.filename)
    filepath = os.path.expanduser("~/" + rel_path)
    directory = os.path.dirname(filepath)
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
else:
    filepath = args.filename + ".bin"
if os.path.isfile(filepath) and not args.overwrite:
    print("File Already exists. Exiting. use --overwrite to ignore")
    exit(1)


file = open(filepath, "wb")

st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
file.write(str(ts).encode())
file.write(b'\n')
RD_LEN = 1024

# print "filepath: " + filepath

print("Take Data (wr 303 300)")
s.send('wr 303 300\r')
s.recv(1024)
if args.spill_length:
    print("Wait "+str(args.spill_length)+" S")
    time.sleep(float(args.spill_length))
else:
    print("Wait 2 S")
    time.sleep(2)
s.send('rd 67\r')
time.sleep(.25)
print("READ 67: ", re.search(r'[0-9A-F]+', s.recv(1024).decode()).group())
count = 0
while True:
    print("Checking if spill done")
    s.send('rd 303\r')
    time.sleep(.1)
    rd303 = re.search(r'[0-9A-F]+', s.recv(1024).decode()).group()
    print("Spill Reg value:", rd303)
    time.sleep(.1)
    s.send('rd 67\r')
    if rd303 == "0000":
        print("Spill Done. 67: ", re.search(
            r'[0-9A-F]+', s.recv(1024).decode()).group())
        break
    count += 1
    print("Spill Not Done. 67: ", re.search(
        r'[0-9A-F]+', s.recv(1024).decode()).group(), " count is:", count)
    time.sleep(1)
s.settimeout(1)
try:
    s.recv(1024)
except:
    print("Ready")
s.send('rdb\r\n')
# s.recv(1024)
for i in range(100000):
    try:
        buf = s.recv(RD_LEN)
    except socket.timeout:
        print("Readout Attempts: ", i-1)
        break
    file.write(buf)

s.close()

print("filepath: " + filepath)
