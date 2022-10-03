# This Python file uses the following encoding: utf-8
# To create the ui for python:
# pyside2-uic form.ui > ui_form.py
import os
from pathlib import Path
import sys

from ui_form import Ui_Widget

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Widget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(Widget, self).__init__()

        self.m_ui = Ui_Widget()
        self.m_ui.setupUi(self)
        self.m_ui.button_movefile.clicked.connect(self.style2_move)
        self.m_ui.button_movefile_5.clicked.connect(self.default_move)
        self.m_ui.pushButton_SetConfig.clicked.connect(self.pressSet)

    def default_move(self):
        QMessageBox.about(self,"tt","m")
        print("hello!")
        run = self.m_ui.run_3.text
        print(run)
    def style2_move(self):
        QMessageBox.about(self,"tt","m")
    def pressSet(self):
        print("hello!")
        self.m_ui.trigger2.setChecked(True)

    def moveFiles(self):
        pass

    def finishRun(self):
        pass

    def saveConfig(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
