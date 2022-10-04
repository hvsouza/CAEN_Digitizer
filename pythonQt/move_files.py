# This Python file uses the following encoding: utf-8
# To create the ui for python:
# pyuic5 -x "../move_files/move_files/mainwindow.ui" -o "ui_mainwindow.py"
import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from config_and_recompile import ConfigRecomp

class MainWindow(QtWidgets.QMainWindow,ConfigRecomp):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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



        self.ui.pushButton_SetConfig.clicked.connect(lambda: self.pressSet())
        self.ui.samplingRate_2.currentTextChanged.connect(lambda:self.twinSample())
        self.ui.pushButtonRecompile.clicked.connect(lambda: self.recompile())

        self.primary = self.ui.primary_name.text()
        self.enable_ch[0].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[0],self.enable_ch[0].isChecked()))
        self.enable_ch[1].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[1],self.enable_ch[1].isChecked()))
        self.enable_ch[2].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[2],self.enable_ch[2].isChecked()))
        self.enable_ch[3].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[3],self.enable_ch[3].isChecked()))
        self.enable_ch[4].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[4],self.enable_ch[4].isChecked()))
        self.enable_ch[5].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[5],self.enable_ch[5].isChecked()))
        self.enable_ch[6].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[6],self.enable_ch[6].isChecked()))
        self.enable_ch[7].clicked.connect(lambda: self.freeTrigger(self.trigger_ch[7],self.enable_ch[7].isChecked()))

        self.ui.FileTypeSet.currentTextChanged.connect(self.changeFormat)
        self.ui.externaltrigger.clicked.connect(self.checkExternalTrigger)
        self.run = 0
        self.subrun = 0
        self.block = ""
        self.extra = ""

        self.getEnableAndTriggerState()

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
        # mpath = "~/Documents/ADC_data/coldbox_data/" + self.primary + "/";
        mpath = "~/Desktop/"+self.primary+"/"
        mkdir = "mkdir -p " + mpath

        folder = "run"+str(self.run)

        oldname = "wave0"
        format = ".txt"
        newname = str(self.subrun)+"_"+oldname
        if self.block != "":
            folder = folder + "_" + self.block
            newname = newname + "_" + self.block

        if self.extra != "":
            newname = newname + "_" + self.extra

        newname = newname + format

        os.system(mkdir)
        mkdir = mkdir + folder
        os.system(mkdir)
        return mkdir,mpath, folder, oldname, newname, format
    def moveFiles(self):
        mkdir, mpath, folder, oldname, newname, format = self.genPatternInfo()

        cmdmv = "mv -n ~/Desktop/" + oldname + format + " " + mpath + folder + "/" + newname
        status = 1
        status = os.system(cmdmv)

        if status == 0:
            QMessageBox.about(self, "", "File was moved, new subrun")
            return True
        else:
            QMessageBox.about(self, "", "ERROR")
            return False

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
