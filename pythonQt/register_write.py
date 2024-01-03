#!/usr/bin/env python3
## ________________________________________ ##
## Author: Henrique Souza
## Filename: register_write.py
## Created: 2023-11-18
## ________________________________________ ##



import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow
from ui_coincidence_trigger import Ui_CoincTrigger
from ui_register import Ui_Register

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class RegisterWritter():
    Register:QtWidgets.QMainWindow
    CoincTrigger:QtWidgets.QMainWindow
    ui:Ui_MainWindow
    regui:Ui_Register
    ctui:Ui_CoincTrigger

    coincEnabledCBox:list
    coinc_enabled:list


    def check_enabled_channels(self):
        cbox:QtWidgets.QCheckBox
        for i, cbox in enumerate(self.coincEnabledCBox):
            if cbox.isChecked():
                self.coinc_enabled[i] = True
                self.enable_ch[i].setChecked(True)
                self.trigger_ch[i].setChecked(True)
                self.ui.externaltrigger.setChecked(False)
            else:
                self.coinc_enabled[i] = False
                self.trigger_ch[i].setChecked(False)

    def check_pair_type(self):
        pair_type:QtWidgets.QComboBox
        auxi = 0
        self.requesting_trigger = []
        for i, pair_type in enumerate(self.triggerTypePair):
            tmp = pair_type.currentText()
            if tmp:
                self.requesting_trigger.append(True)
            else:
                self.requesting_trigger.append(False)
            if tmp == "OR":
                self.data_coinc_pair[i] = 0x03 # or is 11
            elif tmp == "AND":
                self.data_coinc_pair[i] = 0x00 # and is 00
            else:
                bit1 = int(self.coinc_enabled[auxi])     # only ch0 is 01
                bit2 = int(self.coinc_enabled[auxi+1])*2   # only ch1 is 10
                self.data_coinc_pair[i] = bit1+bit2

            auxi+=2


    def coincidenceSet(self):
        self.check_enabled_channels()
        self.check_pair_type()
        self.majority_level = self.ctui.majorityBox.value()
        self.self_trigger_time = self.ctui.self_trg_time.value()
        self.coincidenceWindow = self.ctui.coinc_trg_time.value()
        self.set_self_trigger()
        self.set_trigger_request()
        if self.add_commands_coincidence:
            self.add_commands_coincidence.append(self.place_holder_coincidence_reg)
        self.update_register_list()
        self.writeConfigFile(fromSetConfig=True)
        self.CoincTrigger.close()
        self.CoincTrigger.show()




    def set_self_trigger(self):
        auxi = 0
        self.add_commands_coincidence = []
        for pair, request in zip(self.data_coinc_pair,self.requesting_trigger):
            if not request:
                auxi+=2
                continue
            # set self trigger
            address = f'0x1{auxi}84'
            mask = '0x03' # mask is both channels bits[0:1]
            data = hex(pair)
            cmd = f'WRITE_REGISTER {address} {data} {mask}'
            self.add_commands_coincidence.append(cmd)

            # set self time window
            address = f'0x1{auxi}70'
            mask = '0xFF'
            data = hex(self.self_trigger_time)
            cmd = f'WRITE_REGISTER {address} {data} {mask}'
            self.add_commands_coincidence.append(cmd)
            auxi+=2


    def set_trigger_request(self):
        # setup trigger requests
        address = '0x810C'
        data = 0x00 # all off
        mask = int('0b1111',2)
        list_requests = [0x01, 0x02, 0x04, 0x08] # 0001, 0010, 0010, 1000
        for bitreq, request in zip(list_requests,self.requesting_trigger):
            if request:
                data |= bitreq
        if not data:
            return
        mask = hex(mask)
        data = hex(data)
        cmd = f'WRITE_REGISTER {address} {data} {mask}'
        self.add_commands_coincidence.append(cmd)

        # setup coincidence time
        mask = 0xF00000 # majority at bits 20:23
        bitcoinctime = format(self.coincidenceWindow, '#06b') # force to write 3 as '0b0011' for instance
        data = bin(mask).replace(bin(mask)[:6], bitcoinctime) # use mask to define the bits
        mask = hex(mask)
        data = hex(int(data,2))

        cmd = f'WRITE_REGISTER {address} {data} {mask}'
        self.add_commands_coincidence.append(cmd)

        # setup majority level
        mask = 0x7000000 # majority at bits 24:26
        bitmajority = format(self.majority_level, '#05b') # force to write 3 as '0b011' for instance
        data = bin(mask).replace(bin(mask)[:5], bitmajority) # use mask to define the bits

        mask = hex(mask)
        data = hex(int(data,2))

        cmd = f'WRITE_REGISTER {address} {data} {mask}'
        self.add_commands_coincidence.append(cmd)

    def update_register_list(self):
        currentRegToWrite = self.regui.registers_field.toPlainText().split('\n')
        if currentRegToWrite == ['']:
            currentRegToWrite = []
        idx_reference = 0
        if self.place_holder_coincidence_reg in currentRegToWrite:
            idx_reference = currentRegToWrite.index(self.place_holder_coincidence_reg)
            if idx_reference < len(currentRegToWrite):
                currentRegToWrite = currentRegToWrite[idx_reference+1:]
            else:
                currentRegToWrite = []

        for i, reg in enumerate(self.add_commands_coincidence):
            currentRegToWrite.insert(i,reg)
        self.register_commands = currentRegToWrite

        self.fill_plain_reg(currentRegToWrite)

    def read_register_list(self):
        currentRegToWrite = self.regui.registers_field.toPlainText().split('\n')
        currentRegToWrite = [c for c in currentRegToWrite if c != ''] # remove rogue returns
        self.register_commands = currentRegToWrite
        self.fill_plain_reg(currentRegToWrite) # in case there was rogue returns


    def load_register(self, currentRegWritten):
        self.register_commands = currentRegWritten
        self.fill_plain_reg(currentRegWritten)

    def fill_plain_reg(self, list_of_registers):
        
        plaintext = '\n'.join(list_of_registers)
        self.regui.registers_field.setPlainText(plaintext)




    def controlComboBox(self, idxself, idxpair, idxcombo):
        stateself = self.coincEnabledCBox[idxself].isChecked()
        statepair = self.coincEnabledCBox[idxpair].isChecked()
        if statepair == stateself == True:
            display_options = ["AND", "OR"]
        elif stateself:
            display_options = [f'Only Ch{idxself}']
        elif statepair:
            display_options = [f'Only Ch{idxpair}']
        else:
            display_options = ['']


        combo:QtWidgets.QComboBox
        combo = self.triggerTypePair[idxcombo]
        for i in range(combo.count()):
            combo.removeItem(0)
        for val in display_options:
            combo.insertItem(-1,val)

        combo.setCurrentIndex(0)

        combos:QtWidgets.QComboBox
        nrequests = 0
        for combos in self.triggerTypePair:
            if combos.currentText():
                nrequests+=1
        if nrequests>0:
            self.ctui.majorityBox.setMaximum(nrequests-1)

    def add_register(self):
        address = self.regui.address.text()
        data = self.regui.data.text()
        mask = self.regui.mask.text()
        cmd = f'WRITE_REGISTER {address} {data} {mask}'
        self.read_register_list()
        self.register_commands.append(cmd)
        self.fill_plain_reg(self.register_commands)
        self.regui.address.setText('')
        self.regui.data.setText('')
        self.regui.mask.setText('')

    def toggle_manual_edit_reg(self):
        self.regui.registers_field.setReadOnly(not self.regui.manual_edit.isChecked())


    def clearAllCoinc(self):
        cbox:QtWidgets.QCheckBox
        for i, cbox in enumerate(self.coincEnabledCBox):
            cbox.setChecked(False)
        self.ctui.self_trg_time.setValue(self.ctui.self_trg_time.minimum())
        self.ctui.coinc_trg_time.setValue(self.ctui.coinc_trg_time.minimum())
        if self.place_holder_coincidence_reg in self.register_commands:
            ret = QMessageBox.question(self, "", "Also clear current register commands for coincidence?", QMessageBox.Yes, QMessageBox.No)
            if ret == QMessageBox.Yes:
                self.coincidenceSet() # as all fields are reset, it will right nothing


    def closeRegister(self):
        self.read_register_list()
        self.writeConfigFile(fromSetConfig=True)
        self.Register.close()

    def setRegister(self):
        self.closeRegister()
        self.Register.show()


    def clearRegister(self):
        self.regui.registers_field.setPlainText('')
        self.read_register_list()

def closeRegister(self):
    self.loadConfig
