# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TZD.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(679, 517)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(580, 20, 81, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(90, 0, 361, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btnReceive = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnReceive.setObjectName("btnReceive")
        self.gridLayout.addWidget(self.btnReceive, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        self.btnEnd = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnEnd.setObjectName("btnEnd")
        self.gridLayout.addWidget(self.btnEnd, 1, 1, 1, 1)
        self.btnComm = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnComm.setObjectName("btnComm")
        self.gridLayout.addWidget(self.btnComm, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 20, 31, 23))
        self.label.setObjectName("label")
        self.buttonBox.raise_()
        self.gridLayoutWidget.raise_()
        self.btnComm.raise_()
        self.label.raise_()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnReceive.setText(_translate("Dialog", "开始测量"))
        self.btnEnd.setText(_translate("Dialog", "结束测量"))
        self.btnComm.setText(_translate("Dialog", "连接"))
        self.label.setText(_translate("Dialog", "COM"))

