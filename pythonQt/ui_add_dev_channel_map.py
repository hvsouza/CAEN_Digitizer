# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../move_files/move_files/add_dev_channel_map.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddDev(object):
    def setupUi(self, AddDev):
        AddDev.setObjectName("AddDev")
        AddDev.resize(381, 71)
        AddDev.setMinimumSize(QtCore.QSize(381, 71))
        AddDev.setMaximumSize(QtCore.QSize(381, 71))
        self.centralwidget = QtWidgets.QWidget(AddDev)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.devname = QtWidgets.QLineEdit(self.centralwidget)
        self.devname.setObjectName("devname")
        self.horizontalLayout.addWidget(self.devname)
        self.addb = QtWidgets.QPushButton(self.centralwidget)
        self.addb.setObjectName("addb")
        self.horizontalLayout.addWidget(self.addb)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        AddDev.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AddDev)
        self.statusbar.setObjectName("statusbar")
        AddDev.setStatusBar(self.statusbar)

        self.retranslateUi(AddDev)
        QtCore.QMetaObject.connectSlotsByName(AddDev)

    def retranslateUi(self, AddDev):
        _translate = QtCore.QCoreApplication.translate
        AddDev.setWindowTitle(_translate("AddDev", "Add device"))
        self.label.setText(_translate("AddDev", "Device name"))
        self.addb.setText(_translate("AddDev", "Add"))