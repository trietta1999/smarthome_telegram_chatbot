# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qrcode.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(490, 610)
        MainWindow.setMinimumSize(QtCore.QSize(490, 610))
        MainWindow.setMaximumSize(QtCore.QSize(515, 610))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/background/icon/qr-code.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    border-image: url(:/background/image/qr.png);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.b_qrexit = QtWidgets.QPushButton(self.centralwidget)
        self.b_qrexit.setGeometry(QtCore.QRect(190, 20, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.b_qrexit.setFont(font)
        self.b_qrexit.setObjectName("b_qrexit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mã bí mật"))
        self.b_qrexit.setText(_translate("MainWindow", "Trở về"))
        self.b_qrexit.setShortcut(_translate("MainWindow", "Home, Home Page"))
import rc_rc
