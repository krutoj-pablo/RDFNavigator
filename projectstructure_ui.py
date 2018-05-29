# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\projectstructure.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProjectStructureWidget(object):
    def setupUi(self, ProjectStructureWidget):
        ProjectStructureWidget.setObjectName("ProjectStructureWidget")
        ProjectStructureWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProjectStructureWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.projectTabWidget = QtWidgets.QTabWidget(ProjectStructureWidget)
        self.projectTabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.projectTabWidget.setObjectName("projectTabWidget")
        self.basicStructureTab = QtWidgets.QWidget()
        self.basicStructureTab.setObjectName("basicStructureTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.basicStructureTab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.basicStructureWidget = QtWidgets.QTreeWidget(self.basicStructureTab)
        self.basicStructureWidget.setAnimated(True)
        self.basicStructureWidget.setObjectName("basicStructureWidget")
        self.basicStructureWidget.headerItem().setText(0, "1")
        self.basicStructureWidget.header().setVisible(False)
        self.verticalLayout_2.addWidget(self.basicStructureWidget)
        self.projectTabWidget.addTab(self.basicStructureTab, "")
        self.objectsTab = QtWidgets.QWidget()
        self.objectsTab.setObjectName("objectsTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.objectsTab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.objectsStructureView = QtWidgets.QTreeView(self.objectsTab)
        self.objectsStructureView.setObjectName("objectsStructureView")
        self.verticalLayout_3.addWidget(self.objectsStructureView)
        self.projectTabWidget.addTab(self.objectsTab, "")
        self.fsTab = QtWidgets.QWidget()
        self.fsTab.setObjectName("fsTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.fsTab)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.filesystemTreeView = QtWidgets.QTreeView(self.fsTab)
        self.filesystemTreeView.setAnimated(True)
        self.filesystemTreeView.setObjectName("filesystemTreeView")
        self.verticalLayout_4.addWidget(self.filesystemTreeView)
        self.projectTabWidget.addTab(self.fsTab, "")
        self.verticalLayout.addWidget(self.projectTabWidget)

        self.retranslateUi(ProjectStructureWidget)
        self.projectTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProjectStructureWidget)

    def retranslateUi(self, ProjectStructureWidget):
        _translate = QtCore.QCoreApplication.translate
        ProjectStructureWidget.setWindowTitle(_translate("ProjectStructureWidget", "Form"))
        self.projectTabWidget.setTabText(self.projectTabWidget.indexOf(self.basicStructureTab), _translate("ProjectStructureWidget", "Basic structure"))
        self.projectTabWidget.setTabText(self.projectTabWidget.indexOf(self.objectsTab), _translate("ProjectStructureWidget", "Objects"))
        self.projectTabWidget.setTabText(self.projectTabWidget.indexOf(self.fsTab), _translate("ProjectStructureWidget", "File system"))

