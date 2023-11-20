#!/bin/python3
## ________________________________________ ##
## Author: Henrique Souza
## Filename: move_files.py
## Created: 2022
## ________________________________________ ##

# This Python file uses the following encoding: utf-8
# To create the ui for python:
# pyuic5 -x "../move_files/move_files/mainwindow.ui" -o "ui_mainwindow.py"
import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow
from ui_about import Ui_About
from ui_run_log import Ui_RunLog
from ui_channel_map import Ui_ChannelMap
from ui_add_dev_channel_map import Ui_AddDev
from ui_del_dev_channel_map import Ui_DelDev
from ui_dialog_runlog import Ui_Dialog_RunLog
from ui_coincidence_trigger import Ui_CoincTrigger
from ui_register import Ui_Register

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon


from config_and_recompile import ConfigRecomp
from channel_map import ChannelMapper
from run_log import RunLogger
from register_write import RegisterWritter

from itertools import groupby

import subprocess as sp

from difflib import Differ

class MainWindow(QtWidgets.QMainWindow, ConfigRecomp, ChannelMapper, RunLogger, RegisterWritter):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.nchannels = 8
        self.DEBUGMODE = False
        self.userpath = os.path.expanduser('~') # sames has 'cd ~/ && pwd' but safer
        self.codepath = os.path.abspath(os.path.dirname(__file__)) # gets the location of the python script
        self.codepath_list = self.codepath.split(os.sep) # split it with the division "/",
        self.codepath = os.sep.join(self.codepath_list[:-1]) # remove the last folder

        self.untouch = True # marks if the destination of the data was changed or not
        #configuring some extras
        self.sampling_set = "250 MSamples/s"
        self.sampling_original = "500 MSamples/s"
        self.getPrevState()

        self.ui.samplingRate.setCurrentText(self.sampling_set)
        self.ui.samplingRate_2.setCurrentText(self.sampling_set)
        self.ui.adcMaximumRate.setCurrentText(self.sampling_original)
        self.default_path = f'{self.userpath}/Documents/ADC_data/coldbox_data/'
        self.standard_data_origin = f'{self.userpath}/Desktop/WaveDumpData/'
        self.create_path()
        self.ui.browse_dir.clicked.connect(self.getDir)
        self.primary = self.ui.primary_name.text()
        self.run = [0]
        self.subrun = [0]
        self.block = ""

        self.isprimary = True # set this gui to primary digitizer (in case of 2 in use)

        # Control the moving functions
        self.keep_ask_log = True
        self.nofilesmove = True
        self.ui.button_movefile.clicked.connect(self.style2_move)
        self.ui.button_movefile_5.clicked.connect(self.default_move)
        self.ui.pushButton_2.clicked.connect(lambda: self.finishRun(self.ui.run, self.ui.subrun, 'S'))
        self.ui.pushButton_4.clicked.connect(lambda: self.finishRun(self.ui.run_3, self.ui.subrun3, 'D'))
        self.ui.lock_folder.toggled.connect(self.lock_unlock)
        self.ui.askrunlog.toggled.connect(self.setAskRunLog)

        self.ui.button_movefile_5.setToolTip(self.writeToolTip("D"))
        self.ui.button_movefile.setToolTip(self.writeToolTip("S"))

        self.ui.primary_name.textChanged.connect(lambda: self.updateToolTip("DS"))

        self.ui.run_3.textChanged.connect(lambda: self.updateToolTip("D"))
        self.ui.subrun3.textChanged.connect(lambda: self.updateToolTip("D"))
        self.ui.block1.textChanged.connect(lambda: self.updateToolTip("D"))
        self.ui.block2.textChanged.connect(lambda: self.updateToolTip("D"))

        self.ui.run.textChanged.connect(lambda: self.updateToolTip("S"))
        self.ui.subrun.textChanged.connect(lambda: self.updateToolTip("S"))
        self.ui.voltage.textChanged.connect(lambda: self.updateToolTip("S"))
        self.ui.threshold.textChanged.connect(lambda: self.updateToolTip("S"))
        self.ui.trigger_channel.textChanged.connect(lambda: self.updateToolTip("S"))

        #control config and compile
        self.standard_config_file = "/etc/wavedump/WaveDumpConfig.txt"
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
        self.uitriggertype = [""]

        self.ui.actionAcqusition_only.toggled.connect(lambda: self.setTriggerType("ACQUISITION_ONLY", self.ui.actionAcqusition_only, self.ui.actionAcq_and_TRG_OUT))
        self.ui.actionAcq_and_TRG_OUT.toggled.connect(lambda: self.setTriggerType("ACQUISITION_AND_TRGOUT", self.ui.actionAcq_and_TRG_OUT, self.ui.actionAcqusition_only))

        self.previousStateTrigger = [False for i in range(self.nchannels)]

        self.ui.pushButton_SetConfig.clicked.connect(lambda: self.pressSet())
        self.ui.samplingRate_2.currentTextChanged.connect(lambda:self.twinSample())
        self.ui.adcMaximumRate.currentTextChanged.connect(lambda:self.writeState())
        self.ui.pushButtonRecompile.clicked.connect(lambda: self.recompile())
        self.enable_ch[0].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[0],self.enable_ch[0].isChecked()))
        self.enable_ch[1].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[1],self.enable_ch[1].isChecked()))
        self.enable_ch[2].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[2],self.enable_ch[2].isChecked()))
        self.enable_ch[3].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[3],self.enable_ch[3].isChecked()))
        self.enable_ch[4].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[4],self.enable_ch[4].isChecked()))
        self.enable_ch[5].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[5],self.enable_ch[5].isChecked()))
        self.enable_ch[6].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[6],self.enable_ch[6].isChecked()))
        self.enable_ch[7].stateChanged.connect(lambda: self.freeTrigger(self.trigger_ch[7],self.enable_ch[7].isChecked()))

        self.hold_initial_print = True # do not display message before loading main window
        self.ui.actionLoad_cofig_file.triggered.connect(lambda: self.loadConfig(""))
        self.ui.actionAbout.triggered.connect(self.showAbout)

        self.ui.run_log_b.clicked.connect(self.showRunLog)
        self.ui.channel_map_b.clicked.connect(self.showChannelMap)

        self.ui.FileTypeSet.currentTextChanged.connect(self.changeFormat)
        self.ui.externaltrigger.stateChanged.connect(self.checkExternalTrigger)


        self.About = QtWidgets.QMainWindow()
        self.aui = Ui_About()
        self.aui.setupUi(self.About)
        self.aui.label.setPixmap(QtGui.QPixmap(f"{self.codepath}/.repo_img/computer-nerd.jpg"))
        self.aui.label_2.setOpenExternalLinks(True)


        self.ui.set_data_origin.triggered.connect(self.setDataOrigin)
        self.ui.set_config_file.triggered.connect(self.setConfigFile)
        self.ui.select_as_secondary.toggled.connect(self.setAsSecondary)

        # Channel map Widget setup
        self.ChannelMap = QtWidgets.QMainWindow()
        self.cmui = Ui_ChannelMap()
        self.cmui.setupUi(self.ChannelMap)
        self.ChannelMap.setWindowModality(QtCore.Qt.WindowModality.WindowModal) # prevent window to lose focus (close - open)
        self.ChannelMap.setWindowIcon(QIcon(f"{self.codepath}/.repo_img/icon_GUI.png"))
        self.chmap_neveropen = True
        self.chmap = {0:'', 1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'',}
        self.chmapui = {
            0:self.cmui.chname0,
            1:self.cmui.chname1,
            2:self.cmui.chname2,
            3:self.cmui.chname3,
            4:self.cmui.chname4,
            5:self.cmui.chname5,
            6:self.cmui.chname6,
            7:self.cmui.chname7
        }
        self.define_devices()

        self.cmui.loadmapb.clicked.connect(self.loadSearchMap)
        self.cmui.doneb.clicked.connect(self.doneChannelMap)
        self.cmui.cleanallb.clicked.connect(self.cleanChannelMap)
        self.cmui.adddevb.clicked.connect(self.showAddDev)
        self.cmui.deldevb.clicked.connect(self.showDelDev)
        self.cmui.chname0.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname0,0))
        self.cmui.chname1.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname1,1))
        self.cmui.chname2.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname2,2))
        self.cmui.chname3.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname3,3))
        self.cmui.chname4.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname4,4))
        self.cmui.chname5.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname5,5))
        self.cmui.chname6.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname6,6))
        self.cmui.chname7.currentTextChanged.connect(lambda: self.updateChMap(self.cmui.chname7,7))

        # Run log Widget setup
        self.RunLog = QtWidgets.QMainWindow()
        self.rlui = Ui_RunLog()
        self.rlui.setupUi(self.RunLog)
        self.RunLog.setWindowModality(QtCore.Qt.WindowModality.WindowModal) # prevent window to lose focus (close - open)
        self.RunLog.setWindowIcon(QIcon(f"{self.codepath}/.repo_img/icon_GUI.png"))
        self.runlog_neveropen = True

        self.diag = QtWidgets.QDialog()
        self.diagui = Ui_Dialog_RunLog()
        self.diagui.setupUi(self.diag)

        self.standardlog = "Keep this line or empty to not save"
        self.rlui.loadb.clicked.connect(self.loadSearchRunLog)
        self.rlui.doneb.clicked.connect(self.closeRunLog)


        # Channel map add device
        self.AddDev = QtWidgets.QMainWindow()
        self.adddevui = Ui_AddDev()
        self.adddevui.setupUi(self.AddDev)
        self.AddDev.setWindowModality(QtCore.Qt.WindowModality.WindowModal) # prevent window to lose focus (close - open)
        self.AddDev.setWindowIcon(QIcon(f"{self.codepath}/.repo_img/icon_GUI.png"))
        self.adddevui.addb.clicked.connect(self.addDeviceToMap)

        # Channel map add device
        self.DelDev = QtWidgets.QMainWindow()
        self.deldevui = Ui_DelDev()
        self.deldevui.setupUi(self.DelDev)
        self.DelDev.setWindowModality(QtCore.Qt.WindowModality.WindowModal) # prevent window to lose focus (close - open)
        self.DelDev.setWindowIcon(QIcon(f"{self.codepath}/.repo_img/icon_GUI.png"))
        self.deldevui.delb.clicked.connect(self.delDeviceToMap)

        # Run log Widget setup
        self.CoincTrigger = QtWidgets.QMainWindow()
        self.ctui = Ui_CoincTrigger()
        self.ctui.setupUi(self.CoincTrigger)
        self.CoincTrigger.setWindowModality(QtCore.Qt.WindowModality.WindowModal) # prevent window to lose focus (close - open)
        self.CoincTrigger.setWindowIcon(QIcon(f"{self.codepath}/.repo_img/icon_GUI.png"))

        self.ui.actionCoincidence.triggered.connect(lambda: self.CoincTrigger.show())
        self.coincEnabledCBox = [
            self.ctui.enable0,
            self.ctui.enable1,
            self.ctui.enable2,
            self.ctui.enable3,
            self.ctui.enable4,
            self.ctui.enable5,
            self.ctui.enable6,
            self.ctui.enable7
        ]
        self.triggerTypePair = [
            self.ctui.type01,
            self.ctui.type23,
            self.ctui.type45,
            self.ctui.type67
        ]
        self.coincEnabledCBox[0].stateChanged.connect(lambda: self.controlComboBox(idxself=0, idxpair=1, idxcombo=0))
        self.coincEnabledCBox[1].stateChanged.connect(lambda: self.controlComboBox(idxself=1, idxpair=0, idxcombo=0))
        self.coincEnabledCBox[2].stateChanged.connect(lambda: self.controlComboBox(idxself=2, idxpair=3, idxcombo=1))
        self.coincEnabledCBox[3].stateChanged.connect(lambda: self.controlComboBox(idxself=3, idxpair=2, idxcombo=1))
        self.coincEnabledCBox[4].stateChanged.connect(lambda: self.controlComboBox(idxself=4, idxpair=5, idxcombo=2))
        self.coincEnabledCBox[5].stateChanged.connect(lambda: self.controlComboBox(idxself=5, idxpair=4, idxcombo=2))
        self.coincEnabledCBox[6].stateChanged.connect(lambda: self.controlComboBox(idxself=6, idxpair=7, idxcombo=3))
        self.coincEnabledCBox[7].stateChanged.connect(lambda: self.controlComboBox(idxself=7, idxpair=6, idxcombo=3))

        self.coinc_enabled = [False]*self.nchannels
        self.data_coinc_pair = [0]*(self.nchannels//2)
        self.place_holder_coincidence_reg = '# End of coincidence trigger'
        self.example_reg_reference = "# WRITE_REGISTER 1080 45 FFFFFFFF"

        self.ctui.setb.clicked.connect(self.coincidenceSet)
        self.ctui.clearb.clicked.connect(self.clearAllCoinc)
        self.ctui.cancelb.clicked.connect(lambda: self.CoincTrigger.close())

        # Register Widget setup
        self.Register = QtWidgets.QMainWindow()
        self.regui = Ui_Register()
        self.regui.setupUi(self.Register)
        self.Register.setWindowModality(QtCore.Qt.WindowModality.WindowModal) # prevent window to lose focus (close - open)
        self.Register.setWindowIcon(QIcon(f"{self.codepath}/.repo_img/icon_GUI.png"))

        self.regui.registers_field.setReadOnly(True)
        self.regui.manual_edit.setChecked(False)
        self.regui.manual_edit.clicked.connect(self.toggle_manual_edit_reg)
        self.regui.doneb.clicked.connect(self.closeRegister)
        self.regui.applyb.clicked.connect(self.add_register)

        self.register_commands = ""


        self.majority_level = 0
        self.self_trigger_time = 1
        self.coincidenceWindow = 1

        self.ui.actionRegister.triggered.connect(lambda: self.Register.show())

        # Debug mode button
        self.ui.debugModeBox.toggled.connect(self.setDebugMode)

        # Setup when open
        self.getEnabledAndTrigger()

        self.recordlength = 0
        self.getRecordLength()
        self.loadConfig(self.standard_config_file)
        self.setWindowIcon(QIcon(f"{self.codepath}/.repo_img/icon_GUI.png"))


        
    def closeEvent(self, event):
        self.About.close()
        self.RunLog.close()
        self.ChannelMap.close()
        self.AddDev.close()
        self.Register.close()
        self.CoincTrigger.close()

    def showAbout(self):
        self.About.show()

    def fixGeometry(self, qtwidget:QtWidgets.QMainWindow):
        geo:QtCore.QRect
        geo = qtwidget.geometry()
        qtwidget.setGeometry(
            int(self.geometry().x()+self.geometry().width()/2),
            int(self.geometry().y()+self.geometry().height()/2),
            geo.width(),
            geo.height()
        )

    def showDiagRunLog(self):
        self.diagui.runlogfield.setPlainText(self.rlui.runlogfield.toPlainText())
        ret = self.diag.exec_()
        if ret:
            self.rlui.runlogfield.setPlainText(self.diagui.runlogfield.toPlainText())
        return ret

    def showRunLog(self):
        if self.runlog_neveropen:
            self.fixGeometry(self.RunLog)
            self.runlog_neveropen = False
        self.closeRunLog()
        self.RunLog.show()

    def showChannelMap(self):
        if self.chmap_neveropen:
            self.fixGeometry(self.ChannelMap)
            self.chmap_neveropen = False
        self.ChannelMap.close()
        self.ChannelMap.show()

    def showAddDev(self):
        self.AddDev.show()

    def showDelDev(self):
        self.DelDev.close()
        self.updateDelList()
        self.DelDev.show()

    def showMain(self):
        self.show()

    def setConfigFile(self):
        dirnow = self.ui.primary_name.text()
        mfile, mfilter = QtWidgets.QFileDialog.getOpenFileName(self, "Find Files", f'{self.default_path}/{dirnow}', "*.txt")

        if not mfile: # if nothing was selected, get out
            return

        try:
            with open(mfile,'r') as f:
                # this get content lines and their position
                alllines = [line.rstrip() for line in f]
                lines = [line for line in alllines if line and not line.startswith('#')]
                if lines[0] != '[COMMON]':
                    QMessageBox.critical(self, 'ERROR!!!', f"The file choosen does not seems to be a wavedump configuration file.\nKeeping {self.standard_config_file} as default.")
                    return
        except IOError:
            QMessageBox.critical(self, "ERROR!", "Could not open new config. file")
            return

        self.standard_config_file = mfile
        self.loadConfig(mfile)

    def setDataOrigin(self):
        dirnow = self.ui.primary_name.text()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Find Files", f'{self.default_path}/{dirnow}')
        if directory:
            self.standard_data_origin = f'{directory}/'

    def setAsSecondary(self):
        self.isprimary = not self.ui.select_as_secondary.isChecked()


    def updateToolTip(self, standard):
        if standard != "DS": text = self.writeToolTip(standard)
        if standard == "D": self.ui.button_movefile_5.setToolTip(text)
        elif standard == "S": self.ui.button_movefile.setToolTip(text)
        else:
            text = self.writeToolTip("D")
            self.ui.button_movefile_5.setToolTip(text)
            text = self.writeToolTip("S")
            self.ui.button_movefile.setToolTip(text)

    def writeToolTip(self, standard):
        if standard == "D":
            emptyruns = self.getInfoDefault()
        else:
            emptyruns = self.getInfoStyle2()

        if emptyruns:
            return f'Error: run or subrun is empty'
        _, mpath, folder, _, _, _ = self.genPatternInfo(False)

        return f'Currently folders are going to be transfered to:\n{mpath}{folder}'

    def create_path(self):
        os.system(f'mkdir -p {self.default_path}')
    def getDir(self):
        dirnow = self.ui.primary_name.text()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Find Files", f'{self.default_path}/{dirnow}')
        tocheck = self.default_path[:-1]
        if directory and directory != tocheck:
            if directory.startswith(tocheck):
                directory = directory.replace(self.default_path, '')
                if " " in directory:
                    QMessageBox.warning(self, "WARNING!", "No spaces in the name, they were changed to undercore")
                directory = self.fixString(directory)
                self.ui.primary_name.setText(directory)
            else:
                answer = QMessageBox.Yes
                if self.untouch == True:
                    answer = QMessageBox.critical(self, "ERROR!", f"The data should be kept inside \n{self.default_path}\n Do you want to change it?\n(Please be careful)", QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.Yes:
                    directory = directory+"/"
                    answer2 = QMessageBox.question(self, "", f"Changing the default folder to:\n{directory}\nIs that ok?", QMessageBox.Yes | QMessageBox.No)
                    if answer2 == QMessageBox.Yes:
                        directory = directory.replace(" ","\ ")
                        self.default_path = directory
                        self.untouch = False
        else:
            directory = dirnow
            self.ui.primary_name.setText(directory)
    def saveConfigDefault(self):
        self.getInfoDefault()
        _, mpath, folder, _, _, _ = self.genPatternInfo(False)
        self.saveConfig(mpath+folder)
    def saveConfigStyle2(self):
        self.getInfoStyle2()
        _, mpath, folder, _, _, _ = self.genPatternInfo(False)
        self.saveConfig(mpath+folder)

    def saveConfig(self, pathconfig):
        makequestion = False

        filename = 'config_used.log'
        if not self.isprimary:
            filename = 'config_used_2.log'
        if os.path.exists(f'{pathconfig}/{filename}'):
            with open(f'{pathconfig}/{filename}') as file_1, open(self.standard_config_file) as file_2:
                differ = Differ()
                for line in differ.compare(file_1.readlines(), file_2.readlines()):
                    if line.startswith(("+", "-", "?")):
                        makequestion = True
                        break
                if makequestion:
                    answer = QMessageBox.question(self, "", f"Config. file already exist in this directory with a different setting.\nOverwrite it anyway?", QMessageBox.Yes, QMessageBox.No)
                    if answer == QMessageBox.No:
                        return
        cmdcpy = f"cp {self.standard_config_file} " + pathconfig + f"/{filename}"
        os.system(cmdcpy)
        # QMessageBox.about(self, "", "Config. file saved.")

        self.saveChannelMap(pathconfig)
        self.saveRunLog(pathconfig)


    def fixString(self, mystring):
        mystring_split = mystring.split() # for removing all spaces
        mystring = '_'.join(mystring_split)
        mystring = mystring.replace(".", "_")
        # try: # overdoing it probably
        #     if mystring[-1] == "_":
        #         mystring = mystring[:-1]
        # except IndexError:
        #     pass

        return mystring

    def checkInt(self, val, uival):
        if not uival.text().strip(): # if it is empty or just white spaces
            return True
        try:
            val[0] = int(uival.text())
        except ValueError:
            QMessageBox.critical(self, "ERROR!","Run and Subruns should be unsigned integers")
            uival.undo()
            val[0] = int(uival.text())
            return True

        return False

    def getRunSubrun(self, run, subrun):
        getout = False
        getout = self.checkInt(self.run, run)
        getout = getout or self.checkInt(self.subrun, subrun) # if there is a problem, they return True
        return getout

    def getInfoDefault(self):
        getout = self.getRunSubrun(self.ui.run_3, self.ui.subrun3)
        if getout:
            self.block = ""
            return True

        block1 = self.ui.block1.text()
        block2 = self.ui.block2.text()

        if block1 != "" and block2 != "":
            self.block = block1+"_"+block2
        elif block1 != "":
            self.block = block1
        else:
            self.block = block2
        return False

    def getInfoStyle2(self):
        getout = self.getRunSubrun(self.ui.run, self.ui.subrun)
        if getout:
            self.block = ""
            return True
        voltage = self.ui.voltage.text()
        threshold = self.ui.threshold.text() + "ADC"
        trigger_channel = self.ui.trigger_channel.text()

        voltage_a = voltage.split(".")
        if len(voltage_a) > 1:
            voltage = voltage_a[0] + "V" + voltage_a[1]
        else:
            voltage = voltage_a[0] + "V"

        block = [voltage,threshold,trigger_channel]
        self.block = '_'.join(block)
        return False

    def default_move(self):
        emptyruns = self.getInfoDefault()
        if emptyruns:
            QMessageBox.critical(self, "ERROR", "Run or subrun numbers are empty")
            return
        status = self.moveFiles()
        if status:
            self.saveConfigDefault()
            self.subrun[0] += 1
            self.ui.subrun3.setText(str(self.subrun[0]))
            self.nofilesmove = False

    def style2_move(self):
        emptyruns = self.getInfoStyle2()
        if emptyruns:
            QMessageBox.critical(self, "ERROR", "Run or subrun numbers are empty")
        status = self.moveFiles()
        if status:
            self.saveConfigStyle2()
            self.subrun[0] += 1
            self.ui.subrun.setText(str(self.subrun[0]))
            self.nofilesmove = False




    def genPatternInfo(self, gen = True):
        self.primary = self.ui.primary_name.text()
        # mpath = f"{self.userpath}/Documents/ADC_data/coldbox_data/{self.primary}/"
        mpath = f"{self.default_path}{self.primary}/"
        mkdir = f"mkdir -p {mpath}"

        folder = "run"+str(self.run[0])
        if self.block != "":
            folder = folder + "_" + self.block

        oldname = [f"wave{i}" for i in range(self.nchannels)] # wave0, wave1, etc (normal)
        addidx = 0 if self.isprimary else self.nchannels
        waveN_name = [f"wave{i+addidx}" for i in range(self.nchannels)]

        myformat = self.ui.file_type.text()

        newname = [""]*self.nchannels
        for i, namej in enumerate(waveN_name):

            newname[i] = f'{self.subrun[0]}_{namej}'

            if self.block != "":
                newname[i] = newname[i] + "_" + self.block


            newname[i] = newname[i] + myformat

        if gen: os.system(mkdir)
        mkdir = mkdir + folder
        # will create the daugther folder only when moving
        folder = self.fixString(folder)

        return mkdir, mpath, folder, oldname, newname, myformat


    def getInfoBinary(self, dataname):
        with open(dataname,"rb") as f:
            npts_bytes = f.read(4) #read the 4 first bytes
            bytewvf = int.from_bytes(npts_bytes,sys.byteorder)

        npts = bytewvf - 24
        npts = int(npts/2)

        filesize = os.stat(dataname).st_size
        if bytewvf == 0:
            return 0, 0
        totalwvfs = int(filesize/bytewvf)
        return npts, totalwvfs

    def getInfoASCII(self, dataname):
        with open(dataname,"r") as f:
            npts = f.readline() #read the 4 first bytes

        if npts == "":
            return 0, 0
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

        mkdir, mpath, folder, oldname, newname, myformat = self.genPatternInfo()

        datapath = self.standard_data_origin

        fileIsThere = [False]*self.nchannels
        FileNotThereYet = [True]*self.nchannels
        cmdmv = [""]*self.nchannels
        errorMessage = ""
        errorMessage2 = ""
        messageNpts = ""

        actual_pts_saved = []
        total_events = []
        idx_total_events = []
        aux = 0
        isCritical = False
        for i, _oldname in enumerate(oldname):
            datacheck = datapath+f'{_oldname}{myformat}'
            transfercheck = f'{mpath}{folder}/{newname[i]}'
            fileIsThere[i] = os.path.exists(datacheck)
            FileNotThereYet[i] = not os.path.exists(transfercheck)
            if self.DEBUGMODE:
                cmdmv[i] = f'cp --attributes-only {self.standard_data_origin}{_oldname}{myformat} {mpath}{folder}/{newname[i]}'
            else:
                cmdmv[i] = f'mv -n {self.standard_data_origin}{_oldname}{myformat} {mpath}{folder}/{newname[i]}'



            if self.enable_ch[i].isChecked() and fileIsThere[i] is False:
                errorMessage = f'{errorMessage}Ch{i} is enabled, but has no file !\n'
            elif self.enable_ch[i].isChecked() is False and fileIsThere[i] is False:
                fileIsThere[i] = None
            elif self.enable_ch[i].isChecked() and FileNotThereYet[i] is False:
                errorMessage2 = f'{errorMessage2}The file \'{mpath}{folder}/{newname[i]} \'already exist, please check the run and subrun number!\n'
            elif self.enable_ch[i].isChecked():
                if myformat == ".dat":
                    _actual_pts_saved, _total_events = self.getInfoBinary(datacheck)
                else:
                    _actual_pts_saved, _total_events = self.getInfoASCII(datacheck)
                actual_pts_saved.append(_actual_pts_saved)
                total_events.append(_total_events)
                idx_total_events.append(i)
                if actual_pts_saved[aux] != self.recordsaved:
                    messageNpts = f'{messageNpts}Ch{i} has {actual_pts_saved[aux]} pts per waveforms.\n'
                if len(set(actual_pts_saved))!=1:
                    messageNpts = f'{messageNpts}Number of pts per waveform are not equal in all files!!!\n\nFiles were not transfered.'
                    isCritical = True
                aux += 1

        errorMessage = errorMessage + "Please, check what was the problem with the above files!"
        if False in fileIsThere:
            QMessageBox.critical(self, "ERROR!", errorMessage)
            return False

        if messageNpts != "":
            if(isCritical):
                QMessageBox.critical(self, "ERROR!", messageNpts)
                return False
            else:
                messageNpts = messageNpts + f"According to the last config. set, it should be {self.recordsaved} pts!\nPlease, right this down in a log or correct the mistake."

        messageWvfs = "Channels have different number of wavefors!!!\n\n"
        if self.all_equal(total_events) is False:
            for ch, vals in zip(idx_total_events,total_events):
                messageWvfs = f'{messageWvfs}Ch{ch} had {"{:,}".format(vals)} waveforms recorded\n'
            QMessageBox.critical(self, "ERROR", messageWvfs)
            return False


        if False in FileNotThereYet:
            # for state in FileNotThereYet:
                # print(state)
            QMessageBox.critical(self, "ERROR!", errorMessage2)
            return False


        # create the folder only after checking everying is fine
        os.system(mkdir)

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
            QMessageBox.warning(self, "Warning!", "There are one or more errors transfering the files. Subrun number will change, but check what happend")
        else:
            messageOk = f'{"{:,}".format(total_events[0])} waveforms saved per file.\n\n'
            if messageNpts != "":
                messageOk = f'{messageOk}{messageNpts}\n'

            messageOk = messageOk +'Files were moved, new subrun'
            QMessageBox.about(self, "", messageOk)
        return True

    def finishRun(self, runLine, subrunLine, movetype):
        ret = QMessageBox.question(self, "", "Finish this run?", QMessageBox.Yes, QMessageBox.No)

        if ret == QMessageBox.Yes:
            if movetype == 'D':
                self.getInfoDefault()
            elif movetype == 'S':
                self.getInfoStyle2
            _, mpath, folder, _, _, _ = self.genPatternInfo(False)
            self.saveRunLog(mpath+folder, True)
            QMessageBox.about(self, "", "New run!")
            self.run[0] = int(runLine.text())
            self.run[0] += 1
            runLine.setText(str(self.run[0]))
            self.subrun[0] = 0
            subrunLine.setText(str(self.subrun[0]))
            self.nofilesmove = True


    def lock_unlock(self):
        if self.ui.lock_folder.isChecked():
            self.ui.primary_name.setEnabled(False)
        else:
            self.ui.primary_name.setEnabled(True)

    def setDebugMode(self):
        self.DEBUGMODE = self.ui.debugModeBox.isChecked()



if __name__ == "__main__":
    print("Please, do not close this terminal if you want to recompile wavedump")
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMain()
    sys.exit(app.exec_())
