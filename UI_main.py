# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(665, 535)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/upgrade.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 90, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 130, 641, 51))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(-30, 10, 491, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(48, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_2.setEditable(True)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.comboBox_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 2, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.comboBox_4 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_4.setEditable(True)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox_4)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 3, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 90, 461, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 50, 195, 22))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 65, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget2)
        self.lineEdit_2.setMaxLength(12)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_6.addWidget(self.lineEdit_2)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(160, 50, 103, 22))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_7.setContentsMargins(8, 0, 9, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.comboBox_5 = QtWidgets.QComboBox(self.layoutWidget3)
        self.comboBox_5.setEditable(True)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox_5)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 210, 641, 311))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(False)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_5.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "I型采集器升级软件"))
        self.pushButton_2.setText(_translate("MainWindow", "开始"))
        self.label.setText(_translate("MainWindow", "串口号:"))
        self.label_2.setText(_translate("MainWindow", "波特率:"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "2400"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "9600"))
        self.label_3.setText(_translate("MainWindow", "校验位:"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "E"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "O"))
        self.label_4.setText(_translate("MainWindow", "停止位:"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "1.5"))
        self.pushButton.setText(_translate("MainWindow", "打开"))
        self.label_5.setText(_translate("MainWindow", "地址："))
        self.lineEdit_2.setText(_translate("MainWindow", "aaaaaaaaaaaa"))
        self.label_6.setText(_translate("MainWindow", "长度："))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "256"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "512"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "串口号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "开关"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "状态"))

import ico_rc
