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
        Form.resize(1018, 567)
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
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.btnEnd = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnEnd.setObjectName("btnEnd")
        self.gridLayout.addWidget(self.btnEnd, 1, 1, 1, 1)
        self.btnZero = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnZero.setObjectName("btnZero")
        self.gridLayout.addWidget(self.btnZero, 2, 0, 1, 1)
        self.btnSave = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 2, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(410, 10, 160, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnSetParameters = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btnSetParameters.setObjectName("btnSetParameters")
        self.gridLayout_2.addWidget(self.btnSetParameters, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnReceive.setText(_translate("Form", "开始测量"))
        self.label.setText(_translate("Form", "COM"))
        self.btnEnd.setText(_translate("Form", "结束测量"))
        self.btnZero.setText(_translate("Form", "设置零点数据"))
        self.btnSave.setText(_translate("Form", "保存数据"))
        self.btnSetParameters.setText(_translate("Form", "设置参数"))

from matplotlibwidget import MatplotlibWidget
