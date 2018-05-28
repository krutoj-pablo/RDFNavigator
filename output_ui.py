# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\output.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProjectOutputWidget(object):
    def setupUi(self, ProjectOutputWidget):
        ProjectOutputWidget.setObjectName("ProjectOutputWidget")
        ProjectOutputWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProjectOutputWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.consoleOutputTabWidget = QtWidgets.QTabWidget(ProjectOutputWidget)
        self.consoleOutputTabWidget.setObjectName("consoleOutputTabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.consoleOutputTabWidget.addTab(self.tab, "")
        self.verticalLayout.addWidget(self.consoleOutputTabWidget)

        self.retranslateUi(ProjectOutputWidget)
        self.consoleOutputTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProjectOutputWidget)

    def retranslateUi(self, ProjectOutputWidget):
        _translate = QtCore.QCoreApplication.translate
        ProjectOutputWidget.setWindowTitle(_translate("ProjectOutputWidget", "Form"))
        self.consoleOutputTabWidget.setTabText(self.consoleOutputTabWidget.indexOf(self.tab), _translate("ProjectOutputWidget", "Console output"))

