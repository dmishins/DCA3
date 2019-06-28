# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dmishins/design.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
def setspilllen():
    print "running script to set spill length"
    os.system("python takeBinaryData.py --spill_length " + str(2))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(665, 435)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btn_takespill = QtGui.QPushButton(self.centralwidget)
        self.btn_takespill.setGeometry(QtCore.QRect(240, 240, 88, 29))
        self.btn_takespill.setObjectName(_fromUtf8("btn_takespill"))
        self.btn_setdur = QtGui.QPushButton(self.centralwidget)
        self.btn_setdur.setGeometry(QtCore.QRect(417, 240, 111, 29))
        self.btn_setdur.setObjectName(_fromUtf8("btn_setdur"))
        self.btn_setdur.clicked.connect(setspilllen)

        self.but_exp = QtGui.QPushButton(self.centralwidget)
        self.but_exp.setGeometry(QtCore.QRect(70, 240, 88, 29))
        self.but_exp.setObjectName(_fromUtf8("but_exp"))
        self.btn_setdur.clicked.connect(setspilllen)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 665, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_takespill.setText(_translate("MainWindow", "Take Spill", None))
        self.btn_setdur.setText(_translate("MainWindow", "Set Spill Duration", None))
        self.but_exp.setText(_translate("MainWindow", "export root file", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

