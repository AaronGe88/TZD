# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TZD.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(831, 492)
        self.widget = MatplotlibWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 150, 621, 271))
        self.widget.setObjectName("widget")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btnReceive = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnReceive.setObjectName("btnReceive")
        self.gridLayout.addWidget(self.btnReceive, 1, 0, 1, 1)
        self.btnEnd = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnEnd.setObjectName("btnEnd")
        self.gridLayout.addWidget(self.btnEnd, 1, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnReceive.setText(_translate("Form", "开始测量"))
        self.btnEnd.setText(_translate("Form", "结束测量"))
        self.label.setText(_translate("Form", "COM"))

from matplotlibwidget import MatplotlibWidget
