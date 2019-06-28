

        self.btn_setdur.clicked.connect(self.setspilllen)
        self.btn_takespill.clicked.connect(self.takespill)
        self.btn_exp.clicked.connect(self.exportrootfile)
        self.btn_plt.clicked.connect(self.plot)



    def setspilllen(self):
        print "running script to set spill length"
        #os.system("python takeBinaryData.py --spill_length " + str(2))
        print "python takeBinaryData.py --spill_length " + str(self.spilldurr.value()) + " --command_stop"
    
    def takespill(self):
        print "running take spill"
        #os.system("python takeBinaryData.py --spill_length " + str(2))
        print "python takeBinaryData.py -f " + str(self.binfilename.text())
    
    def exportrootfile(self):
        print "running script to export root file"
        #os.system("python takeBinaryData.py --spill_length " + str(2))
        print "python takeandexportroot.py -lf " + str(self.binfilename.text()) + " --root " + str(self.rootfilename.text())
    def plot(self):
        print "running script to plot data from bin file"

        ch = ""
        super = ""
        fft = ""
        if self.chk_1.checkState():
            ch += "ch1 "
        if self.chk_2.checkState():
            ch += "ch2 "
        if self.chk_3.checkState():
            ch += "ch3 "
        if self.chk_4.checkState():
            ch += "ch4 "
        if self.chk_super.checkState():
            super = "--super "
        if self.chk_fft.checkState():
            fft = "--fft " + ch
        #os.system("python takeBinaryData.py --spill_length " + str(2))
        print "python takeandexportroot.py -lf " + str(self.binfilename.text()) + " -p " + ch + super + fft
