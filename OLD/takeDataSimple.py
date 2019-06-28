import socket   #for sockets
import sys  #for exit
import struct
import time
import datetime

file = open("testfile.txt","w") 

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(('192.168.124.81', 5000))

for j in range(5):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    file.write(st)
    file.write('\n')


    s.send('wr 303 300\r')
    s.recv(1024)
    time.sleep(8)
    s.send('rd 67\r')
    print s.recv(1024)

    s.send('wr 4 0\r')
    s.recv(1024)
    s.send('wr 5 0\r')
    s.recv(1024)

    for i in range(3):
        print "%d %d" % (j, i)
        s.send('rdm 7 400\r\n')
        time.sleep(1)
        buf = s.recv(8192)
        buf = buf.replace(">", "")
        file.write(buf)

    time.sleep(2)

s.close()
