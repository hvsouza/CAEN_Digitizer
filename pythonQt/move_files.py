# This Python file uses the following encoding: utf-8
# To create the ui for python:
# pyside2-uic form.ui > ui_form.py
import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()

        self.m_ui = Ui_MainWindow()
        self.m_ui.setupUi(self)
        self.m_ui.button_movefile.clicked.connect(self.style2_move)
        self.m_ui.button_movefile_5.clicked.connect(self.default_move)
        self.m_ui.pushButton_SetConfig.clicked.connect(self.pressSet)
        self.m_ui.pushButton_2.clicked.connect(lambda:self.finishRun(self.m_ui.run))
        self.m_ui.pushButton_4.clicked.connect(lambda:self.finishRun(self.m_ui.run_3))

        self.primary = self.m_ui.primary_name.text()
        self.m_ui.lock_folder.toggled.connect(self.lock_unlock)

    def default_move(self):
        run = int(self.m_ui.run_3.text())
        subrun = int(self.m_ui.subrun3.text())
        block1 = self.m_ui.block1.text()
        block2 = self.m_ui.block2.text()

        if block1!="" and block2!="":
            block = block1+"_"+block2
        elif block1!="":
            block = block1
        else:
            block = block2
        extra = self.m_ui.extra_3.text()
        status = self.moveFiles(run,subrun,block,extra)
        if status:
            subrun+=1
            subrun=str(subrun)
            self.m_ui.subrun3.setText(subrun)
            QMessageBox.about(self,"","File was moved, new subrun")

    def style2_move(self):
        run = int(self.m_ui.run.text())
        subrun = int(self.m_ui.subrun.text())
        voltage = self.m_ui.voltage.text()
        threshold = self.m_ui.threshold.text() + "ADC"
        trigger_channel = self.m_ui.trigger_channel.text()
        extra = self.m_ui.extra_3.text()

        voltage_a = voltage.split(".")
        if len(voltage_a) > 1:
            voltage = voltage_a[0] + "V" + voltage_a[1]
        else:
            voltage = voltage_a[0] + "V"

        block = [voltage,threshold,trigger_channel]
        block = '_'.join(block)
        status = self.moveFiles(run,subrun,block,extra)
        if status:
            subrun+=1
            subrun=str(subrun)
            self.m_ui.subrun.setText(subrun)


    def pressSet(self):
        print("hello!")
        self.m_ui.trigger2.setChecked(True)

    def moveFiles(self,run,subrun,block,extra):
        self.primary = self.m_ui.primary_name.text()
        # mpath = "~/Documents/ADC_data/coldbox_data/" + self.primary + "/";

        mpath = "~/Desktop/"+self.primary+"/"
        mkdir = "mkdir -p " + mpath

        folder = "run"+str(run)

        oldname = "wave0"
        format = ".txt"
        newname = str(subrun)+"_"+oldname
        if block!="":
            folder = folder + "_" + block
            newname = newname + "_" + block

        if extra!="":
            newname = newname + "_" + extra

        newname = newname + format

        cmdmv = "mv -n ~/Desktop/" + oldname + format + " " + mpath + folder + "/" + newname
        os.system(mkdir)
        mkdir = mkdir+folder
        os.system(mkdir)
        os.system(cmdmv)
        return True

    def finishRun(self,runLine):
        run = int(runLine.text())
        run+=1
        runLine.setText(str(run))

    def saveConfig(self):
        pass

    def lock_unlock(self):
        print("llol")
        if self.m_ui.lock_folder.isChecked():
            self.m_ui.primary_name.setEnabled(False)
        else:
            self.m_ui.primary_name.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
