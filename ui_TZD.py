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
        Form.resize(1317, 652)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(Form)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(20, 20, 1281, 511))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setContentsMargins(-1, -1, 0, 10)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 3, 1, 1)
        self.tableView_force = QtWidgets.QTableView(self.gridLayoutWidget_4)
        self.tableView_force.setObjectName("tableView_force")
        self.gridLayout_4.addWidget(self.tableView_force, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget_4)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.btnSetParameters = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btnSetParameters.setObjectName("btnSetParameters")
        self.horizontalLayout.addWidget(self.btnSetParameters)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_delete_force = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btn_delete_force.setObjectName("btn_delete_force")
        self.gridLayout_3.addWidget(self.btn_delete_force, 0, 1, 1, 1)
        self.btn_apply_force = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btn_apply_force.setObjectName("btn_apply_force")
        self.gridLayout_3.addWidget(self.btn_apply_force, 1, 0, 1, 1)
        self.btn_add_force = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btn_add_force.setObjectName("btn_add_force")
        self.gridLayout_3.addWidget(self.btn_add_force, 0, 0, 1, 1)
        self.btnEnd = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btnEnd.setObjectName("btnEnd")
        self.gridLayout_3.addWidget(self.btnEnd, 1, 2, 1, 1)
        self.btnReceive = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btnReceive.setObjectName("btnReceive")
        self.gridLayout_3.addWidget(self.btnReceive, 0, 2, 1, 1)
        self.btnSave = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout_3.addWidget(self.btnSave, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 2, 1, 1)
        self.widget_flatten = MatplotlibWidget(self.gridLayoutWidget_4)
        self.widget_flatten.setObjectName("widget_flatten")
        self.gridLayout_4.addWidget(self.widget_flatten, 1, 3, 1, 1)
        self.widget_strain = StrainPlotWidget(self.gridLayoutWidget_4)
        self.widget_strain.setObjectName("widget_strain")
        self.gridLayout_4.addWidget(self.widget_strain, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "COM"))
        self.btnSetParameters.setText(_translate("Form", "设置参数"))
        self.btn_delete_force.setText(_translate("Form", "删除"))
        self.btn_apply_force.setText(_translate("Form", "应用"))
        self.btn_add_force.setText(_translate("Form", "添加"))
        self.btnEnd.setText(_translate("Form", "结束测量"))
        self.btnReceive.setText(_translate("Form", "开始测量"))
        self.btnSave.setText(_translate("Form", "保存数据"))

from matplotlibwidget import MatplotlibWidget
from strainplotwidget import StrainPlotWidget
