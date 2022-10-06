#!/usr/bin/env python3

import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class ConfigRecomp():

    def setExternalTrigger(self):
        for var in self.trigger_ch:
            var.setChecked(False)
            var.setDisabled(True)

    def checkExternalTrigger(self):
        if self.ui.externaltrigger.isChecked():
            self.setExternalTrigger()
        else:
            self.getEnabledAndTrigger()
    def changeFormat(self):
        if self.ui.FileTypeSet.currentText() == "Binary":
            self.ui.file_type.setText(".dat")
        else:
            ret = QMessageBox.question(self, "", "Are you sure? Binary is awesome..", QMessageBox.Yes, QMessageBox.No)
            if ret == QMessageBox.Yes:
                QMessageBox.about(self, "", ":(")
                self.ui.file_type.setText(".txt")
            else:
                self.ui.FileTypeSet.setCurrentText("Binary")

    def freeTrigger(self,trigger,state):
        if state and self.ui.externaltrigger.isChecked() is False:
            trigger.setDisabled(False)
        else:
            trigger.setChecked(False)
            trigger.setDisabled(True)

    def getEnabledAndTrigger(self):
        for i, _ch in enumerate(self.enable_ch):
            if _ch.isChecked():
                self.trigger_ch[i].setDisabled(False)
                self.trigger_ch[i].setCheckable(True)
            else:
                self.trigger_ch[i].setChecked(False)
                self.trigger_ch[i].setDisabled(True)

    def getRecordLength(self):
        max_samplingRate = self.ui.adcMaximumRate.currentText()
        max_samplingRate = float(max_samplingRate.split(" ")[0]) # in MSamples/s

        samplingRate = self.ui.samplingRate_2.currentText()
        samplingRate = float(samplingRate.split(" ")[0])

        factor = int(max_samplingRate/samplingRate)

        dtime = 1/samplingRate #already in us
        record_window = float(self.ui.time_in_us.text())

        self.recordsaved = int(round(record_window/dtime)) #this is what is going to be recorded
        if self.recordsaved == 0:
            self.recordsaved = 1
        self.recordlength = int(self.recordsaved*factor) #what is set in the wavedump

        timeCheck = int(record_window*1e3) # time in nano
        samplingCheck = int(dtime*1e3) # in nano
        res = timeCheck%samplingCheck
        ret = self.recordsaved*samplingCheck

        if res != 0:
            QMessageBox.warning(self, "WARNING!!!",f"Time duration and sampling rate are not compatible!\nRecord length set to {self.recordsaved}\nCorresponding to {ret} ns")
    def pressSet(self):
        self.writeConfigFile(True)



    def twinSample(self):
        val = self.ui.samplingRate_2.currentText()
        self.ui.samplingRate.setCurrentText(val)

    def writeConfigFile(self, fromConfig):

        self.getEnabledAndTrigger()
        enabled_ch = [ False for i in range(self.nchannels) ]
        selfTrigger_ch = [ False for i in range(self.nchannels) ]
        selftype = "None (Use \"T\" for continous software trigger)"
        for i, ench in enumerate(self.enable_ch):
            isenabled = ench.isChecked()
            enabled_ch[i] = "YES" if isenabled else "NO"
            isself = self.trigger_ch[i].isChecked()
            selfTrigger_ch[i] = "ACQUISITION_ONLY" if isself else "DISABLED"
            if isself:
                selftype = "Self trigger"

        usbport = int(self.ui.usbPort.text())
        pulse_polarity = self.ui.setPolarity.currentText().upper()
        datatype = self.ui.FileTypeSet.currentText().upper()
        externalTrigger = "ACQUISITION_ONLY" if self.ui.externaltrigger.isChecked() else "DISABLED"
        triggertype = "External trigger" if externalTrigger == "ACQUISITION_ONLY" else selftype
        pulsetype = self.ui.externalType.currentText().upper()

        self.getRecordLength()

        try:

            with open(f"{self.userpath}/Desktop/WaveDumpConfig.txt","w") as f:
                f.write("[COMMON]\n\n")
                f.write(f'OPEN USB {usbport} 0\n\n')
                f.write(f'RECORD_LENGTH  {self.recordlength}\n\n')
                f.write(f'DECIMATION_FACTOR 1\n\n')
                f.write(f'POST_TRIGGER  {self.ui.postTrigger.text()}\n\n')
                f.write(f'PULSE_POLARITY  {pulse_polarity}\n\n')
                f.write(f'EXTERNAL_TRIGGER  {externalTrigger}\n\n')
                f.write(f'FPIO_LEVEL  {pulsetype}\n\n')
                f.write(f'OUTPUT_FILE_FORMAT  {datatype}\n\n')
                f.write(f'OUTPUT_FILE_HEADER  YES\n\n')
                f.write(f'TEST_PATTERN  NO\n\n')
                f.write(f'ENABLE_INPUT  NO\n\n')
                f.write(f'BASELINE_LEVEL  10\n\n')
                f.write(f'TRIGGER_THRESHOLD  100\n\n')
                f.write(f'CHANNEL_TRIGGER  DISABLED\n\n')

                for i in range(self.nchannels):
                    f.write(f'[{i}]\n')
                    f.write(f'ENABLE_INPUT          {enabled_ch[i]}\n')
                    if enabled_ch[i] == "YES":
                        f.write(f'BASELINE_LEVEL        {self.base_ch[i].text()}\n')
                        f.write(f'TRIGGER_THRESHOLD     {self.triggerL_ch[i].text()}\n')
                        f.write(f'CHANNEL_TRIGGER       {selfTrigger_ch[i]}\n')
                    f.write("\n")

        except IOError:
            QMessageBox.critical(self, "ERROR!", "Config. file not opened!")

        message = f'Trigger type: {triggertype}\nRecord length: {self.recordsaved} pts\nPulse polarity: {pulse_polarity}\nFile type: {datatype}'
        if fromConfig:
            message = message + "\nClick 'Ok' and reload wavedump (shift+r)"

        QMessageBox.about(self, "", message)

    def recompile(self):
        nwvfs = self.ui.nwvfs.text()
        if nwvfs == "":
            nwvfs = 10000

        passwrd = self.ui.passwrd.text()

        max_samplingRate = self.ui.adcMaximumRate.currentText()
        max_samplingRate = float(max_samplingRate.split(" ")[0])

        samplingRate = self.ui.samplingRate_2.currentText()
        samplingRate = float(samplingRate.split(" ")[0])

        factor = int(max_samplingRate/samplingRate)

        if factor == 0:
            QMessageBox.critical(self,"ERROR!","ADC Nominal sampling should be higher or equal to Sampling rate !")
            return

        QMessageBox.about(self,"",f'Recompiling wavedump.\n\nSetting {nwvfs} as maximum for continuous writting.\n\nSampling rate set to {samplingRate} MSamples/s.\n\nCheck the terminal for sudo permissions, error messages and progress.')

        validate_sudo = f"printf {passwrd} | sudo -S -v"
        print("Validating...\n")
        result = os.system(validate_sudo)

        if result!=0:
            QMessageBox.critical(self,"ERROR!","Error with sudo permissions, make sure you enter the correct password.\n\nCheck sudo permissions wiht 'sudo -v' on the terminal.")
            print("Press enter to free the terminal...")
            return

        print("\n\n")
        recompile_command = f"bash ~/Documents/CAEN_Digitizer/recompile_wavedump.sh {nwvfs} {factor}"
        os.system(recompile_command)

        print("Press enter to free the terminal...")

        self.writeConfigFile(False);

        QMessageBox.about(self,"","Done!\n\nPlease restart wavedump.");
