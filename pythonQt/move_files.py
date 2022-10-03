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
            QMessageBox.about(self,"","File was moved, new subrun")

    def style2_move(self):
        QMessageBox.about(self,"tt","m")
    def pressSet(self):
        print("hello!")
        self.m_ui.trigger2.setChecked(True)

    def moveFiles(self,run,subrun,block,extra):
        print(f'run{run}_subrun{subrun}_{block}_{extra}')

    def finishRun(self):
        pass

    def saveConfig(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
