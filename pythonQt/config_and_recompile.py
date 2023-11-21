#!/usr/bin/env python3
## ________________________________________ ##
## Author: Henrique Souza
## Filename: config_and_recompile.py
## Created: 2022
## ________________________________________ ##


import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import subprocess as sp

class ConfigRecomp():

    ui:Ui_MainWindow
    def setExternalTrigger(self):
        for var in self.trigger_ch:
            var.setChecked(False)
            var.setDisabled(True)
    def checkExternalTrigger(self):
        if self.ui.externaltrigger.isChecked():
            for i, tr in enumerate(self.trigger_ch):
                self.previousStateTrigger[i] = tr.isChecked()
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

    def freeTrigger(self, trigger, state):
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
                if self.previousStateTrigger[i] == True:
                    self.trigger_ch[i].setChecked(True)
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
        self.writeConfigFile(fromSetConfig=True)
        self.showChannelMap()



    def twinSample(self):
        val = self.ui.samplingRate_2.currentText()
        self.ui.samplingRate.setCurrentText(val)
        self.writeState()


    def checkUSB(self, usbport):
        ret = sp.getoutput("/bin/ls /dev/usb")
        standardret = "v1718_"
        pos = ret.find(standardret)
        if pos == -1: pos = ret.find(standardret.capitalize())
        if pos == -1:
            if not self.hold_initial_print:
                QMessageBox.warning(self, "Warning!", "The digitizer was probably not recognized by the system")
            else:
                self.hold_initial_print = False
            return
        pos += len(standardret)
        realUSB = ret[pos]

        if str(usbport) != realUSB:
            QMessageBox.warning(self, "WARNING", f"The USB port was set to {usbport}.\nThis seems to not be correct.\nIf you have problems running wavedump, try port {realUSB}.")
            return

    def loadConfig(self, mfile):
        if mfile == "":
            dirnow = self.ui.primary_name.text()
            mfile, mfilter = QtWidgets.QFileDialog.getOpenFileName(self, "Find Files", f'{self.default_path}/{dirnow}', "*.txt, *.log")

        if not mfile: # if nothing was selected, get out
            return


        try:

            with open(mfile,"r") as f:
                # this get content lines and their position
                alllines = [line.rstrip() for line in f]
                lines = [line for line in alllines if line and not line.startswith('#')]
                self.ui.usbPort.setValue(int((lines[1].split())[2]))
                self.recordlength = int(lines[2].split()[1])

                max_samplingRate = self.ui.adcMaximumRate.currentText()
                max_samplingRate = float(max_samplingRate.split(" ")[0]) # in MSamples/s

                dtime = 1/max_samplingRate #already in us
                self.ui.time_in_us.setText(str(dtime*self.recordlength))

                self.ui.postTrigger.setText(lines[4].split()[1])
                self.ui.setPolarity.setCurrentText(lines[5].split()[1].capitalize())

                string_exttr = lines[6].split()[1]
                if string_exttr == "ACQUISITION_ONLY":
                    self.ui.externaltrigger.setChecked(True)
                    self.ui.actionAcqusition_only.setChecked(True)
                elif string_exttr == "ACQUISITION_AND_TRGOUT":
                    self.ui.externaltrigger.setChecked(True)
                    self.ui.actionAcq_and_TRG_OUT.setChecked(True)
                    # self.setExternalTrigger()
                else:
                    self.ui.externaltrigger.setChecked(False)

                self.ui.externalType.setCurrentText(lines[7].split()[1])
                self.ui.FileTypeSet.setCurrentText(lines[8].split()[1])

                channel = 0
                current_channel = 0
                for i in range(9, len(lines)):
                    try:
                        second_input = lines[i].split()[1]
                    except:
                        second_input = ""

                    if lines[i].startswith(f'[{current_channel}]'):
                        channel = current_channel
                        current_channel+=1
                    elif lines[i].startswith("ENABLE_INPUT"):
                        if second_input == "YES":
                            self.enable_ch[channel].setChecked(True)
                        else:
                            self.enable_ch[channel].setChecked(False)
                            # self.freeTrigger(self.trigger_ch[channel], True)
                    elif lines[i].startswith("BASELINE"):
                        self.base_ch[channel].setText(second_input)
                    elif lines[i].startswith("TRIGGER_THRESHOLD"):
                        self.triggerL_ch[channel].setText(second_input)
                    elif lines[i].startswith("CHANNEL_TRIGGER"):
                        if second_input != "DISABLED" and self.trigger_ch[channel].isEnabled():
                            self.uitriggertype[0] = second_input
                            if self.uitriggertype[0] == "ACQUISITION_ONLY":
                                self.ui.actionAcqusition_only.setChecked(True)
                            else:
                                self.ui.actionAcq_and_TRG_OUT.setChecked(True)
                            self.trigger_ch[channel].setChecked(True)
                        else:
                            self.trigger_ch[channel].setChecked(False)



                for ch in range(current_channel, self.nchannels):
                    self.enable_ch[ch].setChecked(False)
                    self.trigger_ch[ch].setChecked(False)

        except IOError:
            QMessageBox.critical(self, "ERROR!", "Config. file not opened!")
            return
        self.writeConfigFile(fromSetConfig=False)

    def writeConfigFile(self, fromSetConfig):

        enabled_ch = [ False for i in range(self.nchannels) ]
        selfTrigger_ch = [ False for i in range(self.nchannels) ]
        selftype = "None (Use \"T\" for continous software trigger)"
        for i, ench in enumerate(self.enable_ch):
            isenabled = ench.isChecked()
            enabled_ch[i] = "YES" if isenabled else "NO"
            isself = self.trigger_ch[i].isChecked()
            selfTrigger_ch[i] = self.uitriggertype[0] if isself else "DISABLED"
            if isself:
                selftype = "Self trigger"

        usbport = int(self.ui.usbPort.text())

        self.checkUSB(usbport)


        pulse_polarity = self.ui.setPolarity.currentText().upper()
        datatype = self.ui.FileTypeSet.currentText().upper()
        if self.ui.actionAcqusition_only.isChecked():
            self.uitriggertype[0] = "ACQUISITION_ONLY"
        else:
            self.uitriggertype[0] = "ACQUISITION_AND_TRGOUT"

        externalTrigger = self.uitriggertype[0] if self.ui.externaltrigger.isChecked() else "DISABLED"
        triggertype = "External trigger" if externalTrigger != "DISABLED" else selftype
        pulsetype = self.ui.externalType.currentText().upper()

        self.getRecordLength()

        config_field = [""]*15
        config_field[0] = '[COMMON]'
        config_field[1] = 'OPEN USB'
        config_field[2] = 'RECORD_LENGTH'
        config_field[3] = 'DECIMATION_FACTOR'
        config_field[4] = 'POST_TRIGGER'
        config_field[5] = 'PULSE_POLARITY'
        config_field[6] = 'EXTERNAL_TRIGGER'
        config_field[7] = 'FPIO_LEVEL'
        config_field[8] = 'OUTPUT_FILE_FORMAT'
        config_field[9] = 'OUTPUT_FILE_HEADER'
        config_field[10] = 'TEST_PATTERN'
        config_field[11] = 'ENABLE_INPUT'
        config_field[12] = 'BASELINE_LEVEL'
        config_field[13] = 'TRIGGER_THRESHOLD'
        config_field[14] = 'CHANNEL_TRIGGER'


        replace = [""]*15
        replace[0]  = f'{config_field[0]}'
        replace[1]  = f'{config_field[1]} {usbport} 0'
        replace[2]  = f'{config_field[2]}  {self.recordlength}'
        replace[3]  = f'{config_field[3]} 1'
        replace[4]  = f'{config_field[4]}  {self.ui.postTrigger.text()}'
        replace[5]  = f'{config_field[5]}  {pulse_polarity}'
        replace[6]  = f'{config_field[6]}  {externalTrigger}'
        replace[7]  = f'{config_field[7]}  {pulsetype}'
        replace[8]  = f'{config_field[8]}  {datatype}'
        replace[9]  = f'{config_field[9]}  YES'
        replace[10] = f'{config_field[10]}  NO'
        replace[11] = f'{config_field[11]}  NO'
        replace[12] = f'{config_field[12]}  10'
        replace[13] = f'{config_field[13]}  100'
        replace[14] = f'{config_field[14]}  DISABLED'
        replace_ch = []

        basenow = [0]*self.nchannels
        triggerLnow  = [0]*self.nchannels

        for i, (base, trigger) in enumerate(zip(self.base_ch, self.triggerL_ch)):

            basenow[i] = int(round(float(base.text())))
            if basenow[i]>100 or basenow[i]<0:
                QMessageBox.critical(self, "ERROR!", "Baseline level range from 0 to 100 (integer)")
                return
            triggerLnow[i] = int(round(float(trigger.text())))

            base.setText(str(basenow[i]))
            trigger.setText(str(triggerLnow[i]))


        for i in range(self.nchannels):
            chconf = []
            chconf.append(f'[{i}]')
            chconf.append(f'\n')
            chconf.append(f'ENABLE_INPUT          {enabled_ch[i]}\n')
            if basenow[i] == "":
                basenow[i] = 10
            if triggerLnow[i] == "":
                triggerLnow[i] = 10
            if selfTrigger_ch[i] == "":
                selfTrigger_ch[i] = "DISABLED"
            chconf.append(f'BASELINE_LEVEL        {basenow[i]}\n')
            chconf.append(f'TRIGGER_THRESHOLD     {triggerLnow[i]}\n')
            chconf.append(f'CHANNEL_TRIGGER       {selfTrigger_ch[i]}\n')

            chconf.append("\n")
            replace_ch.append(chconf)

        try:

            with open(self.standard_config_file, "r+") as f:
                # this get content lines and their position
                alllines = [line.rstrip() for line in f]


                # Clean up registers, because we main increase or decrease those.
                # Keep old self.register_commands or update when reading config file
                register_command = []
                tmplines = []
                for i, line in enumerate(alllines):
                    if line.startswith(("WRITE_REGISTER", "ADDRESS", "DATA", "MASK")) or line.startswith(self.place_holder_coincidence_reg):
                        register_command.append(line)
                    else:
                        tmplines.append(line)

                alllines  = tmplines
                lines = [line for line in alllines if line and not line.startswith('#')]

                if not fromSetConfig:
                    self.load_register(register_command)

                # add again registers
                idx_registers = alllines.index(self.example_reg_reference) + 1
                for reg in self.register_commands:
                    
                    alllines.insert(idx_registers, reg)
                    idx_registers+=1

                # replace the common structure of the file
                idxstart = 0
                for rep, cfield in zip(replace, config_field):
                    for i, line in enumerate(alllines[idxstart:]):
                        if line.startswith(cfield):
                            alllines[i+idxstart] = rep
                            idxstart = i+idxstart
                            break

                # search for the calling of the channel '[x]', keep whatwever is written there
                # this is good to keep something such as '[0] # detector 2'
                firstpos = 0
                for i in range(self.nchannels):
                    for j, line in enumerate(alllines):
                        if line.startswith(replace_ch[i][0]):
                            if i == 0:
                                firstpos = j
                            replace_ch[i][0] = line

                # if firstpos == 0: firstpos = pos
                f.seek(0)
                f.truncate(0)
                for i, line in enumerate(alllines):
                    if i < firstpos:
                        f.write(f'{line}\n')

                for rep in replace_ch:
                    for line in rep:
                        f.write(line)


        except IOError:
            QMessageBox.critical(self, "ERROR!", "Config. file not opened!")

        message = f'Trigger type: {triggertype}\nRecord length: {self.recordsaved} pts\nPulse polarity: {pulse_polarity}\nFile type: {datatype}'
        if fromSetConfig:
            message = message + "\nClick 'Ok' and reload wavedump (shift+r)"
            QMessageBox.about(self, "", message)

    def recompile(self):
        nwvfs = self.ui.nwvfs.text()
        if nwvfs == "":
            nwvfs = 10000

        passwrd = self.ui.passwrd.text()

        max_samplingRate = self.ui.adcMaximumRate.currentText()
        self.sampling_original = max_samplingRate
        max_samplingRate = float(max_samplingRate.split(" ")[0])

        samplingRate = self.ui.samplingRate_2.currentText()
        self.sampling_set = samplingRate
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
        recompile_command = f"bash {self.codepath}/recompile_wavedump.sh {nwvfs} {factor}"
        os.system(recompile_command)

        print("Press enter to free the terminal...")

        self.writeConfigFile(False);

        QMessageBox.about(self,"","Done!\n\nPlease restart wavedump.");
        self.writeState()


    def getPrevState(self):

        filestate = f"{self.codepath}/pythonQt/.state"
        try:
            with open(filestate,"r") as f:
                # this get content lines and their position
                alllines = [line.rstrip() for line in f]
                lines = [line for line in alllines if line and not line.startswith('#')]
                self.sampling_set = lines[0]
                self.sampling_original = lines[1]

        except IOError:
            self.writeState()

    def writeState(self):
        filestate = f"{self.codepath}/pythonQt/.state"
        self.sampling_original = self.ui.adcMaximumRate.currentText()
        self.sampling_set = self.ui.samplingRate_2.currentText()
        try:
            with open(filestate,"w") as f:
                f.write(f'# Sampling rate set\n')
                f.write(f'{self.sampling_set}\n')
                f.write(f'# Sampling rate original\n')
                f.write(f'{self.sampling_original}\n')
        except IOError:
            return


    def setTriggerType(self, typechoice, uichoice, uiotherchoice):
        # as soon as it is clicked, The state changes, keep this in mind
        # self.ui = Ui_MainWindow()
        if uiotherchoice.isChecked() and uichoice.isChecked(): #just activated uichoice
            self.uitriggertype[0] = typechoice
            uiotherchoice.setChecked(False)
        elif not uiotherchoice.isChecked() and not uichoice.isChecked():
            uichoice.setChecked(True)
            QMessageBox.about(self, "WARNING", f'{typechoice} was kept.\nChoose one of the two trigger types.')
            self.uitriggertype[0] = typechoice
