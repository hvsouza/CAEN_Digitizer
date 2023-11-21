#!/usr/bin/env python3
## ________________________________________ ##
## Author: Henrique Souza
## Filename: channel_map.py
## Created: 2023-11-07
## ________________________________________ ##


import os
from pathlib import Path
import sys

from ui_mainwindow import Ui_MainWindow
from ui_channel_map import Ui_ChannelMap
from ui_add_dev_channel_map import Ui_AddDev
from ui_del_dev_channel_map import Ui_DelDev

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import subprocess as sp
import csv

class ChannelMapper():
    ChannelMap:QtWidgets.QMainWindow
    ui:Ui_MainWindow
    cmui:Ui_ChannelMap
    adddevui:Ui_AddDev
    deldevui:Ui_DelDev

    chmap:dict
    chmapui:dict


    def doneChannelMap(self):
        self.retrieveChannelMap()
        self.ChannelMap.close()

    def updateChMap(self, chk_ui:QtWidgets.QComboBox, k):
        val:QtWidgets.QComboBox
        currentText = chk_ui.currentText()
        if len(currentText.split('(IN USE)')) > 1:
            chk_ui.setCurrentIndex(0)
            return
        self.chmap[k] = currentText

        for key, val in self.chmapui.items():
            currentidx = val.currentIndex()
            currenttext = val.currentText().split('(IN USE) ')[-1]
            for i in range(val.count()):
                chopt = val.itemText(i).split('(IN USE) ')[-1]
                if not chopt.strip(): continue
                if chopt in self.chmap.values() and chopt != currenttext:
                    val.setItemText(i,f'(IN USE) {chopt}')
                else:
                    val.setItemText(i, chopt)



                


    def retrieveChannelMap(self):
        v:QtWidgets.QComboBox
        for k, v in self.chmapui.items():
            if v.currentText() in self.alldevs:
                self.chmap[k] = v.currentText()
                if len(self.chmap[k].split('(IN USE)')) > 1:
                    QMessageBox.critical(self, "ERROR!", "This error should never pop !!!!\nClick at the question mark and send some feedback email please")
            else:
                v.setCurrentIndex(0)
                self.chmap[k] = ''

    def loadSearchMap(self):
        dirnow = self.ui.primary_name.text()
        mfile, mfilter = QtWidgets.QFileDialog.getOpenFileName(self, "Find Files", f'{self.default_path}/{dirnow}', "*.log")
        self.showChannelMap()

        if not mfile: # if nothing was selected, get out
            return

        self.loadChannelMap(mfile)
        flag_update_dev = False
        for k, v in self.chmap.items():
            dev_:str
            dev_ = v
            if not dev_.split(): continue
            if dev_.capitalize() not in self.alldevs_cap:
                ret = QMessageBox.question(self, "", f"Device {dev_} not in the main list. Add it ?", QMessageBox.Yes, QMessageBox.No)
                if ret == QMessageBox.Yes:
                    flag_update_dev = True
                    self.alldevs = set(self.alldevs)
                    self.alldevs.add(dev_)
                    self.alldevs = sorted(self.alldevs)
                    self.alldevs_cap.add(dev_.capitalize())
                else:
                    self.chmap[k] = ''
                self.showChannelMap()
            if dev_ not in self.alldevs:
                for devs in self.alldevs:
                    if dev_.capitalize() == devs:
                        self.chmap[k] = devs


                
        self.fillItemsMap()
        if flag_update_dev:
            self.updateMapListFile()


    def loadChannelMap(self, fmapchannel):
        try:
            with open(fmapchannel, newline='') as csvfile:
                linedump = csv.DictReader(csvfile, delimiter=',')
                for x in linedump:
                    if 'name' not in x or 'channel' not in x:
                        QMessageBox.warning(self, "Error!", "File is not compatible with channel map")
                        self.showChannelMap()
                        return
                csvfile.seek(0)
                linedump = csv.DictReader(csvfile, delimiter=',')
                self.cleanChannelMap()
                for x in linedump:
                    chname = x['name']
                    self.chmap[int(x['channel'])] = chname
        except IOError:
            QMessageBox.critical(self, "ERROR!", "Channel map file not opened!")
            return

    def updateDelList(self):
        for i in range(self.deldevui.devname.count()):
            self.deldevui.devname.removeItem(0)

        self.deldevui.devname.insertItem(0,'')
        for i, dev_ in enumerate(self.alldevs):
            self.deldevui.devname.insertItem(i+1, dev_)
        self.deldevui.devname.setCurrentIndex(0)


    def delDeviceToMap(self):
        deldev = self.deldevui.devname.currentText()
        if deldev == '':
            QMessageBox.about(self, "No deleted item", "Cannot delete what does not exist")
            self.showDelDev()
            return

        self.alldevs.pop(self.alldevs.index(deldev))
        self.alldevs_cap = set(self.alldevs)
        self.fillItemsMap()
        self.DelDev.close()
        self.updateMapListFile()




    def addDeviceToMap(self):
        newdev = self.getNewDevName()
        self.alldevs = set(self.alldevs)
        if newdev.split():
            if newdev.capitalize() in self.alldevs_cap:
                QMessageBox.warning(self, "WARNING!!!", "Device already exist! Check capitalization.")
            else:
                self.alldevs.add(newdev)
                self.alldevs_cap.add(newdev.capitalize())
                self.alldevs = sorted(self.alldevs)
                self.fillItemsMap()
                self.adddevui.devname.setText('')
        self.AddDev.close()
        self.updateMapListFile()
        self.showChannelMap()

    def getNewDevName(self):
        flag_message = False
        tmpdev = self.adddevui.devname.text()
        newdev = self.fixString(tmpdev)
        if (tmpdev != newdev and tmpdev[-1] != ' '):
            flag_message = True

        if flag_message:
            QMessageBox.warning(self, "Warning!", "Don't use space or points. They where replaced by underscore!")

        return newdev

    def cleanChannelMap(self):
        for k, v in self.chmapui.items():
            v.setCurrentIndex(0)

    def updateMapListFile(self):
        try:
            with open(self.filedevice,"w") as f:
                for v in self.alldevs:
                    if v.strip():
                        f.write(v+"\n")

        except IOError:
            QMessageBox.critical(self, "ERROR!", "Could not save the devices name")

    def saveChannelMap(self, pathconfig):

        filename = 'channelmap.log'
        if not self.isprimary:
            filename = 'channelmap_2.log'

        fchmap = f'{pathconfig}/{filename}'
        nametowrite = []
        chtowrite = []
        all_empty = True
        for i in range(self.nchannels):
            if self.enable_ch[i].isChecked():
                nametowrite.append(self.chmap[i])
                chtowrite.append(i)
                if self.chmap[i].split():
                    all_empty = False

        if not all_empty:
            for i, (chidx, name) in enumerate(zip(chtowrite,nametowrite)):
                if not name.split():
                    QMessageBox.warning(self, "WARNING!!!", f"Ch.{chidx} has no name set")
        else:
            return



        if os.path.exists(fchmap):
            dumpnames = []
            try:
                with open(fchmap, newline='') as csvfile:
                    linedump = csv.DictReader(csvfile, delimiter=',')
                    for x in linedump:
                        dumpnames.append(x['name'])
            except IOError:
                QMessageBox.critical(self, "ERROR!", "Something went wrong :x")
            if dumpnames != nametowrite:
                answer = QMessageBox.question(self, "", f"Channel map file already exist in this directory with a different map.\nOverwrite it anyway?", QMessageBox.Yes, QMessageBox.No)
                if answer == QMessageBox.No:
                    return

        try:
            with open(fchmap,'w') as f:
                f.write('idx,channel,name\n')
                for i, (chidx, name) in enumerate(zip(chtowrite, nametowrite)):
                    f.write(f'{i},{chidx},{name}\n')
        except IOError:
            QMessageBox.critical(self, "ERROR!", "Could not save the channel map")

    def define_devices(self):
        self.filedevice = f"{self.codepath}/pythonQt/.devices"
        self.alldevs = set()
        self.alldevs_cap = set()
        v:QtWidgets.QComboBox
        
        try:
            with open(self.filedevice,"r") as f:
                Lines = f.readlines()
                for i, line in enumerate(Lines):
                    line = line.strip() # remove break line
                    self.alldevs.add(line)
                    self.alldevs_cap.add(line.capitalize())

            self.alldevs = sorted(self.alldevs)
            self.fillItemsMap()

        except IOError:
            with open(self.filedevice,"w") as f:
                f.write(' \n')

    def fillItemsMap(self):
        v:QtWidgets.QComboBox
        for k, v in self.chmapui.items():
            tmpdev = self.chmap[k]
            for i in range(v.count()):
                v.removeItem(0) # it will realocate to zero!
            v.insertItem(0, '')
            for i, dev in enumerate(self.alldevs):
                v.insertItem(i+1, dev)

            v.setCurrentText(tmpdev)
