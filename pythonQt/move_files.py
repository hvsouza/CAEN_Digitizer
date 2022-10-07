# This Python file uses the following encoding: utf-8
# To create the ui for python:
# pyuic5 -x "../move_files/move_files/mainwindow.ui" -o "ui_mainwindow.py"
import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog


from config_and_recompile import ConfigRecomp
from itertools import groupby

import subprocess as sp

class MainWindow(QtWidgets.QMainWindow,ConfigRecomp):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.nchannels = 8
        self.userpath = os.path.expanduser('~') # sames has 'cd ~/ && pwd' but safer
        #configuring some extras
        self.ui.samplingRate.setCurrentText("250 MSamples/s")
        self.ui.samplingRate_2.setCurrentText("250 MSamples/s")

        # Control the moving functions
        self.ui.button_movefile.clicked.connect(self.style2_move)
        self.ui.button_movefile_5.clicked.connect(self.default_move)
        self.ui.pushButton_2.clicked.connect(lambda: self.finishRun(self.m_ui.run))
        self.ui.pushButton_4.clicked.connect(lambda: self.finishRun(self.m_ui.run_3))
        self.ui.lock_folder.toggled.connect(self.lock_unlock)
        self.ui.button_save_config_2.clicked.connect(self.saveConfigDefault)
        self.ui.button_save_config.clicked.connect(self.saveConfigStyle2)

        #control config and compile
        self.enable_ch = [
            self.ui.enable1,
            self.ui.enable2,
            self.ui.enable3,
            self.ui.enable4,
            self.ui.enable5,
            self.ui.enable6,
            self.ui.enable7,
            self.ui.enable8,
        ]

        self.trigger_ch = [
            self.ui.trigger1,
            self.ui.trigger2,
            self.ui.trigger3,
            self.ui.trigger4,
            self.ui.trigger5,
            self.ui.trigger6,
            self.ui.trigger7,
            self.ui.trigger8,
        ]

        self.base_ch = [
            self.ui.base1,
            self.ui.base2,
            self.ui.base3,
            self.ui.base4,
            self.ui.base5,
            self.ui.base6,
            self.ui.base7,
            self.ui.base8,
        ]

        self.triggerL_ch = [
            self.ui.triggerL1,
            self.ui.triggerL2,
            self.ui.triggerL3,
            self.ui.triggerL4,
            self.ui.triggerL5,
            self.ui.triggerL6,
            self.ui.triggerL7,
            self.ui.triggerL8,
        ]

        self.previousStateTrigger = [False for i in range(self.nchannels)]

        self.ui.pushButton_SetConfig.clicked.connect(lambda: self.pressSet())
        self.ui.samplingRate_2.currentTextChanged.connect(lambda:self.twinSample())
        self.ui.pushButtonRecompile.clicked.connect(lambda: self.recompile())
        self.default_path = f'{self.userpath}/Documents/ADC_data/coldbox_data/'
        self.ui.browse_dir.clicked.connect(self.getDir)
        self.primary = self.ui.primary_name.text()
        self.enable_ch[0].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[0],self.enable_ch[0].isChecked()))
        self.enable_ch[1].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[1],self.enable_ch[1].isChecked()))
        self.enable_ch[2].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[2],self.enable_ch[2].isChecked()))
        self.enable_ch[3].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[3],self.enable_ch[3].isChecked()))
        self.enable_ch[4].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[4],self.enable_ch[4].isChecked()))
        self.enable_ch[5].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[5],self.enable_ch[5].isChecked()))
        self.enable_ch[6].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[6],self.enable_ch[6].isChecked()))
        self.enable_ch[7].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[7],self.enable_ch[7].isChecked()))

        self.ui.FileTypeSet.currentTextChanged.connect(self.changeFormat)
        self.ui.externaltrigger.stateChanged.connect(self.checkExternalTrigger)
        self.run = 0
        self.subrun = 0
        self.block = ""
        self.extra = ""

        self.getEnabledAndTrigger()

        self.recordlength = 0
        self.getRecordLength()
        self.loadConfig()

    def getDir(self):
        dirnow = self.ui.primary_name.text()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Find Files",
                                                               f'{self.default_path}/{dirnow}')
        tocheck = self.default_path[:-1]
        if directory and directory != tocheck:
            if directory.startswith(tocheck):
                directory = directory.replace(self.default_path, '')
                if " " in directory:
                    QMessageBox.warning(self, "WARNING!", "No spaces in the name, they were changed to undercore")
                directory = self.fixString(directory)
                self.ui.primary_name.setText(directory)
            else:
                answer = QMessageBox.critical(self, "ERROR!", f"The data should be kept inside \n{self.default_path}\n Do you want to change it?\n(Please be careful)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    directory = directory+"/"
                    answer2 = QMessageBox.question(self, "", f"Changing the default folder to:\n{directory}\nIs that ok?", QMessageBox.Yes | QMessageBox.No)
                    if answer2 == QMessageBox.Yes:
                        self.default_path = directory
        else:
            directory = "new_data"
            self.ui.primary_name.setText(directory)
    def saveConfigDefault(self):
        self.getInfoDefault()
        _, mpath, folder, _, _, _ = self.genPatternInfo()
        self.saveConfig(mpath+folder)
    def saveConfigStyle2(self):
        self.getInfoStyle2()
        _, mpath, folder, _, _, _ = self.genPatternInfo()
        self.saveConfig(mpath+folder)

    def saveConfig(self, pathconfig):
        cmdcpy = "cp /etc/wavedump/WaveDumpConfig.txt " + pathconfig + "/config_used.log"
        os.system(cmdcpy)

    def fixString(self, string):
        string = string.replace(" ", "_")
        string = string.replace(".", "_")
        return string

    def getInfoDefault(self):
        self.run = int(self.ui.run_3.text())
        self.subrun = int(self.ui.subrun3.text())
        block1 = self.ui.block1.text()
        block2 = self.ui.block2.text()

        if block1 != "" and block2 != "":
            self.block = block1+"_"+block2
        elif block1 != "":
            self.block = block1
        else:
            self.block = block2
        self.extra = self.ui.extra_3.text()

    def getInfoStyle2(self):
        self.run = int(self.ui.run.text())
        self.subrun = int(self.ui.subrun.text())
        voltage = self.ui.voltage.text()
        threshold = self.ui.threshold.text() + "ADC"
        trigger_channel = self.ui.trigger_channel.text()
        self.extra = self.ui.extra_3.text()

        voltage_a = voltage.split(".")
        if len(voltage_a) > 1:
            voltage = voltage_a[0] + "V" + voltage_a[1]
        else:
            voltage = voltage_a[0] + "V"

        block = [voltage,threshold,trigger_channel]
        self.block = '_'.join(block)

    def default_move(self):
        self.getInfoDefault()
        status = self.moveFiles()
        if status:
            self.subrun += 1
            self.ui.subrun3.setText(str(self.subrun))

    def style2_move(self):
        self.getInfoStyle2()
        status = self.moveFiles()
        if status:
            self.subrun += 1
            self.ui.subrun.setText(str(self.subrun))




    def genPatternInfo(self):
        self.primary = self.ui.primary_name.text()
        # mpath = f"{self.userpath}/Documents/ADC_data/coldbox_data/{self.primary}/"
        mpath = f"{self.default_path}{self.primary}/"
        mkdir = f"mkdir -p {mpath}"

        folder = "run"+str(self.run)
        if self.block != "":
            folder = folder + "_" + self.block

        oldname = [f"wave{i}" for i in range(self.nchannels)]
        format = self.ui.file_type.text()

        newname = [""]*self.nchannels
        for i, namej in enumerate(oldname):

            newname[i] = f'{self.subrun}_{namej}'

            if self.block != "":
                newname[i] = newname[i] + "_" + self.block

            if self.extra != "":
                newname[i] = newname[i] + "_" + self.extra

            newname[i] = newname[i] + format

        os.system(mkdir)
        mkdir = mkdir + folder
        os.system(mkdir)

        return mkdir,mpath, folder, oldname, newname, format


    def getInfoBinary(self, dataname):
        with open(dataname,"rb") as f:
            npts_bytes = f.read(4) #read the 4 first bytes
            bytewvf = int.from_bytes(npts_bytes,sys.byteorder)

        npts = bytewvf - 24
        npts = int(npts/2)

        filesize = os.stat(dataname).st_size
        totalwvfs = int(filesize/bytewvf)
        return npts, totalwvfs

    def getInfoASCII(self, dataname):
        with open(dataname,"r") as f:
            npts = f.readline() #read the 4 first bytes

        npts = int(npts.rsplit()[2])
        nlines = sp.getoutput(f'wc -l {dataname}')
        npts = int(npts)
        nlines = int(nlines.split(' ')[0])

        totalwvfs = int(nlines/(npts+7))
        return npts, totalwvfs

    def all_equal(self,iterator):
        g = groupby(iterator)
        return next(g, True) and not next(g, False)

    def moveFiles(self):

        self.block = self.fixString(self.block)
        self.extra =self.fixString(self.extra)

        mkdir, mpath, folder, oldname, newname, format = self.genPatternInfo()

        datapath = f'{self.userpath}/Desktop/WaveDumpData/'

        fileIsThere = [False]*self.nchannels
        FileNotThereYet = [True]*self.nchannels
        cmdmv = [""]*self.nchannels
        errorMessage = ""
        errorMessage2 = ""
        messageNpts = ""

        actual_pts_saved = []
        total_events = []
        idx_total_events = []
        for i, _oldname in enumerate(oldname):
            datacheck = datapath+f'{_oldname}{format}'
            transfercheck = f'{mpath}{folder}/{newname[i]}'
            fileIsThere[i] = os.path.exists(datacheck)
            FileNotThereYet[i] = not os.path.exists(transfercheck)
            cmdmv[i] = f'mv -n ~/Desktop/WaveDumpData/{_oldname}{format} {mpath}{folder}/{newname[i]}'


            if self.enable_ch[i].isChecked() and fileIsThere[i] is False:
                errorMessage = f'{errorMessage}Ch{i} is enabled, but has no file !\n'
            elif self.enable_ch[i].isChecked() is False and fileIsThere[i] is False:
                fileIsThere[i] = None
            elif self.enable_ch[i].isChecked() and FileNotThereYet[i] is False:
                errorMessage2 = f'{errorMessage2}The file \'{mpath}{folder}/{newname[i]} \'already exist, please check the run and subrun number!\n'
            elif self.enable_ch[i].isChecked():
                if format == ".dat":
                    _actual_pts_saved, _total_events = self.getInfoBinary(datacheck)
                else:
                    _actual_pts_saved, _total_events = self.getInfoASCII(datacheck)
                actual_pts_saved.append(_actual_pts_saved)
                total_events.append(_total_events)
                idx_total_events.append(i)
                if actual_pts_saved[i] != self.recordsaved:
                    messageNpts = f'{messageNpts}Ch{i} has {actual_pts_saved[i]} pts per waveforms.\n'

        if messageNpts != "":
            messageNpts = messageNpts + f"According to the last config. set, it should be {self.recordsaved} pts! Please, right this down in a log."
            # QMessageBox.critical(self, "ERROR!", f'{messageNpts}\n\n Check the sampling rate configuration')
            # return False

        messageWvfs = "Channels have different number of wavefors!!!\n\n"
        if self.all_equal(total_events) is False:
            for ch, vals in zip(idx_total_events,total_events):
                messageWvfs = f'{messageWvfs}Ch{ch} had {vals} recorded\n'
            QMessageBox.critical(self, "ERROR", messageWvfs)
            return False

        errorMessage = errorMessage + "Please, check what was the protblem with the above files!"
        if False in fileIsThere:
            QMessageBox.critical(self, "ERROR!", errorMessage)
            return False

        if False in FileNotThereYet:
            # for state in FileNotThereYet:
                # print(state)
            QMessageBox.critical(self, "ERROR!", errorMessage2)
            return False

        noerror = []
        for c, e in zip(cmdmv,self.enable_ch):
            if e.isChecked():
                # status = 0
                status = os.system(c)
                if status != 0:
                    QMessageBox.about(self, "", f"ERROR {status}")
                    noerror.append(False)
                else:
                    noerror.append(True)

        if False in noerror:
            QMessageBox.warning(self, "Warning!", "There one or more errors transfering the files. Subrun number will change, but check what happend")
        else:
            messageOk = f'{"{:,}".format(total_events[0])} waveforms saved per file.\n\n'
            if messageNpts != "":
                messageOk = f'{messageOk}{messageNpts}\n'

            messageOk = messageOk +'Files were moved, new subrun'
            QMessageBox.about(self, "", messageOk)
        return True

    def finishRun(self, runLine):
        ret = QMessageBox.question(self, "", "Finish this run?", QMessageBox.Yes, QMessageBox.No)

        if ret == QMessageBox.Yes:
            QMessageBox.about(self, "", "New run!")
            self.run = int(runLine.text())
            self.run += 1
            runLine.setText(str(self.run))


    def lock_unlock(self):
        if self.ui.lock_folder.isChecked():
            self.ui.primary_name.setEnabled(False)
        else:
            self.ui.primary_name.setEnabled(True)



if __name__ == "__main__":
    print("Please, do not close this terminal if you want to recompile wavedump")
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())