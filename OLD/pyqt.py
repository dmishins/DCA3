import sys
import os
from PyQt4 import QtGui, QtCore
#import takeBinaryData
def sayhi():
	print "hi"
	os.system("echo nbhi ")

app = QtGui.QApplication(sys.argv)

window = QtGui.QWidget()
window.setGeometry(50,50,500,300)
window.setWindowTitle("hi")
btn = QtGui.QPushButton("Quit", window)
os.system("echo my ")
btn.clicked.connect(os.system("python takeBinaryData.py --spill_length " + str(2)))

window.show()
print "here"

sys.exit(app.exec_())