# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OLD/DAPHNEgui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(364, 351)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_takespill = QtWidgets.QPushButton(self.centralwidget)
        self.btn_takespill.setGeometry(QtCore.QRect(10, 100, 88, 29))
        self.btn_takespill.setObjectName("btn_takespill")
        self.btn_setdur = QtWidgets.QPushButton(self.centralwidget)
        self.btn_setdur.setGeometry(QtCore.QRect(10, 50, 111, 29))
        self.btn_setdur.setObjectName("btn_setdur")
        self.btn_exp = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exp.setGeometry(QtCore.QRect(10, 140, 88, 29))
        self.btn_exp.setObjectName("btn_exp")
        self.spilldurr = QtWidgets.QSpinBox(self.centralwidget)
        self.spilldurr.setGeometry(QtCore.QRect(200, 50, 59, 29))
        self.spilldurr.setObjectName("spilldurr")
        self.rootfilename = QtWidgets.QLineEdit(self.centralwidget)
        self.rootfilename.setGeometry(QtCore.QRect(200, 140, 113, 29))
        self.rootfilename.setObjectName("rootfilename")
        self.label_root_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_root_filename.setGeometry(QtCore.QRect(110, 150, 81, 17))
        self.label_root_filename.setObjectName("label_root_filename")
        self.binfilename = QtWidgets.QLineEdit(self.centralwidget)
        self.binfilename.setGeometry(QtCore.QRect(200, 100, 113, 29))
        self.binfilename.setObjectName("binfilename")
        self.label_bin_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_bin_filename.setGeometry(QtCore.QRect(110, 110, 81, 17))
        self.label_bin_filename.setObjectName("label_bin_filename")
        self.chk_super = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_super.setGeometry(QtCore.QRect(190, 220, 141, 21))
        self.chk_super.setObjectName("chk_super")
        self.btn_plt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_plt.setGeometry(QtCore.QRect(10, 210, 101, 29))
        self.btn_plt.setObjectName("btn_plt")
        self.chk_fft = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_fft.setGeometry(QtCore.QRect(190, 240, 86, 22))
        self.chk_fft.setObjectName("chk_fft")
        self.chk_maxadchist = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_maxadchist.setGeometry(QtCore.QRect(190, 260, 141, 22))
        self.chk_maxadchist.setObjectName("chk_maxadchist")
        self.chk_areahist = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_areahist.setGeometry(QtCore.QRect(190, 280, 131, 22))
        self.chk_areahist.setObjectName("chk_areahist")
        self.chk_plot = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_plot.setGeometry(QtCore.QRect(190, 200, 86, 22))
        self.chk_plot.setObjectName("chk_plot")
        self.btn_measurecur = QtWidgets.QPushButton(self.centralwidget)
        self.btn_measurecur.setGeometry(QtCore.QRect(10, 10, 111, 29))
        self.btn_measurecur.setObjectName("btn_measurecur")
        self.current_channel = QtWidgets.QSpinBox(self.centralwidget)
        self.current_channel.setGeometry(QtCore.QRect(200, 10, 59, 29))
        self.current_channel.setObjectName("current_channel")
        self.plainTextEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 270, 104, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 250, 40, 12))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 364, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.btn_setdur.clicked.connect(self.setspilllen)
        self.btn_measurecur.clicked.connect(self.getcurrent)
        self.btn_takespill.clicked.connect(self.takespill)
        self.btn_exp.clicked.connect(self.exportrootfile)
        self.btn_plt.clicked.connect(self.plot)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DAPHNE GUI"))
        self.btn_takespill.setText(_translate("MainWindow", "Take Spill"))
        self.btn_setdur.setText(_translate("MainWindow", "Set Spill Duration"))
        self.btn_exp.setText(_translate("MainWindow", "export root file"))
        self.label_root_filename.setText(_translate("MainWindow", "root Filename"))
        self.label_bin_filename.setText(_translate("MainWindow", "Bin Filename"))
        self.chk_super.setText(_translate("MainWindow", "superimpose events"))
        self.btn_plt.setText(_translate("MainWindow", "Plot from bin file"))
        self.chk_fft.setText(_translate("MainWindow", "fft"))
        self.chk_maxadchist.setText(_translate("MainWindow", "MAX adc Histogram"))
        self.chk_areahist.setText(_translate("MainWindow", "Area Histogram"))
        self.chk_plot.setText(_translate("MainWindow", "Plot"))
        self.btn_measurecur.setText(_translate("MainWindow", "Measure Current"))
        self.label.setText(_translate("MainWindow", "Channel"))


    def setspilllen(self):
        print("running script to set spill length")
        print("python takeBinaryData.py --spill_length " + str(self.spilldurr.value()) + " --command_stop")

        os.system("python takeBinaryData.py --spill_length " + str(self.spilldurr.value()) + " --command_stop")
    
    def getcurrent(self):
        print("running script to set spill length")
        print("python takeBinaryData.py --get_current " + str(self.current_channel.value()) + " --command_stop")

        os.system("python takeBinaryData.py --get_current " + str(self.current_channel.value()) + " --command_stop")

    def takespill(self):
        print("running take spill")
        print("python takeBinaryData.py -f " + str(self.binfilename.text()))
        os.system("python takeBinaryData.py -f " + str(self.binfilename.text()))

    def exportrootfile(self):
        print("running script to export root file")     
        print("python takeandexportroot.py " + str(self.binfilename.text()) + " --root " + str(self.rootfilename.text()))

        os.system("python takeandexportroot.py " + str(self.binfilename.text()) + " --root " + str(self.rootfilename.text()))
    def plot(self):
        print("running script to plot data from bin file")

        ch = ""
        super = ""
        fft = ""
        ahist = ""
        hist = ""
        plot = ""
        ch =self.plainTextEdit.text()
        if self.chk_super.checkState():
            super = " --super "
        if self.chk_fft.checkState():
            fft = " --fft " + ch
        if self.chk_areahist.checkState():
            ahist = " --ahist " + ch
        if self.chk_maxadchist.checkState():
            hist = " --hist " + ch
        if self.chk_plot.checkState():
            plot  = " -p " + ch


        print("python takeandexportroot.py " + str(self.binfilename.text()) + plot + super + fft + ahist + hist + " --ignore_timestamp")

        os.system("python takeandexportroot.py " + str(self.binfilename.text()) + plot + super + fft + ahist + hist + " --ignore_timestamp")



if __name__ == "__main__":

    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
        def __init__(self, *args, obj=None, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)
            self.setupUi(self)

    import sys
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()



