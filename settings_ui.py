# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\settings_dlg.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(659, 190)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingsDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.settingsGroupBox = QtWidgets.QGroupBox(SettingsDialog)
        self.settingsGroupBox.setObjectName("settingsGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.settingsGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rdfToolsPathLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.rdfToolsPathLabel.setObjectName("rdfToolsPathLabel")
        self.gridLayout_2.addWidget(self.rdfToolsPathLabel, 0, 0, 1, 1)
        self.rdfToolslineEdit = QtWidgets.QLineEdit(self.settingsGroupBox)
        self.rdfToolslineEdit.setObjectName("rdfToolslineEdit")
        self.gridLayout_2.addWidget(self.rdfToolslineEdit, 0, 1, 1, 1)
        self.rdfToolsBrowseButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.rdfToolsBrowseButton.setObjectName("rdfToolsBrowseButton")
        self.gridLayout_2.addWidget(self.rdfToolsBrowseButton, 0, 2, 1, 1)
        self.pluginsPathLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.pluginsPathLabel.setObjectName("pluginsPathLabel")
        self.gridLayout_2.addWidget(self.pluginsPathLabel, 1, 0, 1, 1)
        self.pluginsLineEdit = QtWidgets.QLineEdit(self.settingsGroupBox)
        self.pluginsLineEdit.setObjectName("pluginsLineEdit")
        self.gridLayout_2.addWidget(self.pluginsLineEdit, 1, 1, 1, 1)
        self.pluginsBrowseButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.pluginsBrowseButton.setObjectName("pluginsBrowseButton")
        self.gridLayout_2.addWidget(self.pluginsBrowseButton, 1, 2, 1, 1)
        self.schemaPathLabel = QtWidgets.QLabel(self.settingsGroupBox)
        self.schemaPathLabel.setObjectName("schemaPathLabel")
        self.gridLayout_2.addWidget(self.schemaPathLabel, 2, 0, 1, 1)
        self.schemaLineEdit = QtWidgets.QLineEdit(self.settingsGroupBox)
        self.schemaLineEdit.setObjectName("schemaLineEdit")
        self.gridLayout_2.addWidget(self.schemaLineEdit, 2, 1, 1, 1)
        self.schemaBrowseButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.schemaBrowseButton.setObjectName("schemaBrowseButton")
        self.gridLayout_2.addWidget(self.schemaBrowseButton, 2, 2, 1, 1)
        self.schemaPathLabel_2 = QtWidgets.QLabel(self.settingsGroupBox)
        self.schemaPathLabel_2.setObjectName("schemaPathLabel_2")
        self.gridLayout_2.addWidget(self.schemaPathLabel_2, 3, 0, 1, 1)
        self.sysDataLineEdit = QtWidgets.QLineEdit(self.settingsGroupBox)
        self.sysDataLineEdit.setObjectName("sysDataLineEdit")
        self.gridLayout_2.addWidget(self.sysDataLineEdit, 3, 1, 1, 1)
        self.sysDataBrowseButton = QtWidgets.QPushButton(self.settingsGroupBox)
        self.sysDataBrowseButton.setObjectName("sysDataBrowseButton")
        self.gridLayout_2.addWidget(self.sysDataBrowseButton, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.settingsGroupBox, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Dialog"))
        self.settingsGroupBox.setTitle(_translate("SettingsDialog", "RDF navigator settings"))
        self.rdfToolsPathLabel.setText(_translate("SettingsDialog", "RDF Tools path:"))
        self.rdfToolsBrowseButton.setText(_translate("SettingsDialog", "Browse"))
        self.pluginsPathLabel.setText(_translate("SettingsDialog", "Plugins Path:"))
        self.pluginsBrowseButton.setText(_translate("SettingsDialog", "Browse"))
        self.schemaPathLabel.setText(_translate("SettingsDialog", "Schema Path:"))
        self.schemaBrowseButton.setText(_translate("SettingsDialog", "Browse"))
        self.schemaPathLabel_2.setText(_translate("SettingsDialog", "System data Path:"))
        self.sysDataBrowseButton.setText(_translate("SettingsDialog", "Browse"))

import rdfnavigator_rc
