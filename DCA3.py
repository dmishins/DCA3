# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DAPHNEgui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 453)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_takespill = QtWidgets.QPushButton(self.centralwidget)
        self.btn_takespill.setGeometry(QtCore.QRect(20, 230, 88, 29))
        self.btn_takespill.setObjectName("btn_takespill")
        self.btn_setdur = QtWidgets.QPushButton(self.centralwidget)
        self.btn_setdur.setGeometry(QtCore.QRect(20, 90, 111, 29))
        self.btn_setdur.setObjectName("btn_setdur")
        self.btn_exp = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exp.setGeometry(QtCore.QRect(120, 230, 88, 29))
        self.btn_exp.setObjectName("btn_exp")
        self.spilldurr = QtWidgets.QSpinBox(self.centralwidget)
        self.spilldurr.setGeometry(QtCore.QRect(150, 90, 59, 29))
        self.spilldurr.setObjectName("spilldurr")
        self.rootfilename = QtWidgets.QLineEdit(self.centralwidget)
        self.rootfilename.setGeometry(QtCore.QRect(310, 230, 113, 29))
        self.rootfilename.setObjectName("rootfilename")
        self.label_root_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_root_filename.setGeometry(QtCore.QRect(220, 240, 81, 17))
        self.label_root_filename.setObjectName("label_root_filename")
        self.binfilename = QtWidgets.QLineEdit(self.centralwidget)
        self.binfilename.setGeometry(QtCore.QRect(150, 140, 113, 29))
        self.binfilename.setObjectName("binfilename")
        self.label_bin_filename = QtWidgets.QLabel(self.centralwidget)
        self.label_bin_filename.setGeometry(QtCore.QRect(70, 150, 81, 17))
        self.label_bin_filename.setObjectName("label_bin_filename")
        self.chk_super = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_super.setGeometry(QtCore.QRect(20, 320, 141, 21))
        self.chk_super.setObjectName("chk_super")
        self.btn_plt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_plt.setGeometry(QtCore.QRect(20, 280, 101, 29))
        self.btn_plt.setObjectName("btn_plt")
        self.chk_fft = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_fft.setGeometry(QtCore.QRect(260, 300, 86, 22))
        self.chk_fft.setObjectName("chk_fft")
        self.chk_maxadchist = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_maxadchist.setGeometry(QtCore.QRect(260, 320, 141, 22))
        self.chk_maxadchist.setObjectName("chk_maxadchist")
        self.chk_areahist = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_areahist.setGeometry(QtCore.QRect(260, 340, 131, 22))
        self.chk_areahist.setObjectName("chk_areahist")
        self.chk_plot = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_plot.setGeometry(QtCore.QRect(260, 280, 86, 22))
        self.chk_plot.setObjectName("chk_plot")
        self.btn_measurecur = QtWidgets.QPushButton(self.centralwidget)
        self.btn_measurecur.setGeometry(QtCore.QRect(20, 190, 111, 29))
        self.btn_measurecur.setObjectName("btn_measurecur")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(140, 280, 104, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.btn_measurecur_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_measurecur_2.setGeometry(QtCore.QRect(300, 190, 131, 29))
        self.btn_measurecur_2.setObjectName("btn_measurecur_2")
        self.btn_setupboard = QtWidgets.QPushButton(self.centralwidget)
        self.btn_setupboard.setGeometry(QtCore.QRect(20, 10, 111, 29))
        self.btn_setupboard.setObjectName("btn_setupboard")
        self.btn_setv = QtWidgets.QPushButton(self.centralwidget)
        self.btn_setv.setGeometry(QtCore.QRect(20, 50, 111, 29))
        self.btn_setv.setObjectName("btn_setv")
        self.label_voltage_ch = QtWidgets.QLabel(self.centralwidget)
        self.label_voltage_ch.setGeometry(QtCore.QRect(150, 10, 71, 21))
        self.label_voltage_ch.setObjectName("label_voltage_ch")
        self.label_voltage_value = QtWidgets.QLabel(self.centralwidget)
        self.label_voltage_value.setGeometry(QtCore.QRect(290, 30, 81, 17))
        self.label_voltage_value.setObjectName("label_voltage_value")
        self.label_voltage_ch_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_voltage_ch_2.setGeometry(QtCore.QRect(150, 30, 121, 21))
        self.label_voltage_ch_2.setObjectName("label_voltage_ch_2")
        self.btn_readadc = QtWidgets.QPushButton(self.centralwidget)
        self.btn_readadc.setGeometry(QtCore.QRect(230, 90, 111, 29))
        self.btn_readadc.setObjectName("btn_readadc")
        self.label_voltage_ch_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_voltage_ch_3.setGeometry(QtCore.QRect(150, 170, 141, 21))
        self.label_voltage_ch_3.setObjectName("label_voltage_ch_3")
        self.text_v_ch = QtWidgets.QLineEdit(self.centralwidget)
        self.text_v_ch.setGeometry(QtCore.QRect(150, 50, 113, 29))
        self.text_v_ch.setObjectName("text_v_ch")
        self.text_v_val = QtWidgets.QLineEdit(self.centralwidget)
        self.text_v_val.setGeometry(QtCore.QRect(290, 50, 131, 29))
        self.text_v_val.setObjectName("text_v_val")
        self.label_voltage_ch_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_voltage_ch_4.setGeometry(QtCore.QRect(140, 260, 61, 21))
        self.label_voltage_ch_4.setObjectName("label_voltage_ch_4")
        self.chk_darkrate = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_darkrate.setGeometry(QtCore.QRect(260, 360, 131, 22))
        self.chk_darkrate.setObjectName("chk_darkrate")
        self.chk_pseudogain = QtWidgets.QCheckBox(self.centralwidget)
        self.chk_pseudogain.setGeometry(QtCore.QRect(260, 380, 131, 22))
        self.chk_pseudogain.setObjectName("chk_pseudogain")
        self.current_channel = QtWidgets.QLineEdit(self.centralwidget)
        self.current_channel.setGeometry(QtCore.QRect(140, 190, 151, 31))
        self.current_channel.setObjectName("current_channel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 442, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.btn_setdur.clicked.connect(self.setspilllen)
        self.btn_measurecur.clicked.connect(self.getcurrent)
        self.btn_measurecur_2.clicked.connect(self.plotcurrent)
        self.btn_takespill.clicked.connect(self.takespill)
        self.btn_exp.clicked.connect(self.exportrootfile)
        self.btn_plt.clicked.connect(self.plot)
        self.btn_setupboard.clicked.connect(self.setupboard)
        self.btn_setv.clicked.connect(self.setv)
        self.btn_readadc.clicked.connect(self.readadc)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DAPHNE GUI"))
        self.btn_takespill.setText(_translate("MainWindow", "Take Spill"))
        self.btn_setdur.setText(_translate("MainWindow", "Set Spill Duration"))
        self.btn_exp.setText(_translate("MainWindow", "export root file"))
        self.label_root_filename.setText(_translate("MainWindow", "root Filename"))
        self.label_bin_filename.setText(_translate("MainWindow", "Run Name/No:"))
        self.chk_super.setText(_translate("MainWindow", "superimpose events"))
        self.btn_plt.setText(_translate("MainWindow", "Plot Spill"))
        self.chk_fft.setText(_translate("MainWindow", "fft"))
        self.chk_maxadchist.setText(_translate("MainWindow", "MAX adc Histogram"))
        self.chk_areahist.setText(_translate("MainWindow", "Area Histogram"))
        self.chk_plot.setText(_translate("MainWindow", "Plot"))
        self.btn_measurecur.setText(_translate("MainWindow", "Measure Current"))
        self.btn_measurecur_2.setText(_translate("MainWindow", "Plot Current Measurement"))
        self.btn_setupboard.setText(_translate("MainWindow", "Setup Board"))
        self.btn_setv.setText(_translate("MainWindow", "Set Voltage"))
        self.label_voltage_ch.setText(_translate("MainWindow", "V. Reg. Addr"))
        self.label_voltage_value.setText(_translate("MainWindow", "Voltage"))
        self.label_voltage_ch_2.setText(_translate("MainWindow", "(-1=all, ex. 445=ch24-31)"))
        self.btn_readadc.setText(_translate("MainWindow", "Read voltage ADC"))
        self.label_voltage_ch_3.setText(_translate("MainWindow", "ch. (-1=all), or space sep. list"))
        self.label_voltage_ch_4.setText(_translate("MainWindow", "ch. (-1=all)"))
        self.chk_darkrate.setText(_translate("MainWindow", "Dark Rate"))
        self.chk_pseudogain.setText(_translate("MainWindow", "Pseudo-Gain"))

    def do(str):
        print(str)
        os.system(str)

    def setupboard(self):
        print("running script to setup board")
        do("python takeBinaryData.py --setup " + " --command_stop")

    def setv(self):
        print("Setting voltage")
        do("python takeBinaryData.py --set_voltage " + str(self.text_v_val.text()) + " --v_ch " + str(self.text_v_ch.text()) + " --command_stop")

    def readadc(self):
        print("Reading ADC: ")
        do("python takeBinaryData.py --read_voltage --command_stop")
    def setspilllen(self):
        print("running script to set spill length")
        print("python takeBinaryData.py --spill_length " + str(self.spilldurr.text()) + " --command_stop")

        os.system("python takeBinaryData.py --spill_length " + str(self.spilldurr.text()) + " --command_stop")
    
    def plotcurrent(self):
        print("running script to plot current")     
        print("python takeandexportroot.py " + str(self.binfilename.text()) + " --plota0 ")
        os.system("python takeandexportroot.py " + str(self.binfilename.text()) + " --plota0 ")

    def getcurrent(self):
        print("running script to take current measurement")
        print("python takeBinaryData.py --get_current " + str(self.current_channel.text()) + " --command_stop")

        os.system("python takeBinaryData.py --get_current " + str(self.current_channel.text()) + " --command_stop")

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
