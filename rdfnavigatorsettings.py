# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:18:53 2018

@author: z003umpb
"""

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QFileDialog

from settings_ui import Ui_SettingsDialog

class RDFNavigatorSettings(QtWidgets.QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        super(RDFNavigatorSettings, self).__init__(parent)
        self.setupUi(self)
        self.rdfToolsBrowseButton.clicked.connect(self.getRDFToolsPath)
        self.pluginsBrowseButton.clicked.connect(self.getPluginsPath)
        self.schemaBrowseButton.clicked.connect(self.getSchemaPath)
        self.sysDataBrowseButton.clicked.connect(self.getSysDataPath)
        self.config_dict = {}
    
    def getConfig(self):
        return self.config_dict
    
    def getRDFToolsPath(self):
        path = QFileDialog.getExistingDirectory(self, "Get RDF tools directory", '/home/', QFileDialog.ShowDirsOnly)
        self.config_dict['rdf_tools'] = path
        self.rdfToolslineEdit.setText(path)
    
    def getPluginsPath(self):
        path = QFileDialog.getExistingDirectory(self, "Get RDF plugins directory", '/home/', QFileDialog.ShowDirsOnly)
        self.config_dict['rdf_plugins'] = path
        self.pluginsLineEdit.setText(path)
        
    def setPluginsPath(self, configs):
        self.pluginsLineEdit.setText(configs.getConfig('rdf_plugins', '') if configs.hasConfig('rdf_plugins') else '')
    
    def setRDFToolsPath(self, configs):
        self.rdfToolslineEdit.setText(configs.getConfig('rdf_tools', '') if configs.hasConfig('rdf_tools') else '')

    def getSchemaPath(self):
        path = QFileDialog.getExistingDirectory(self, "Get RDF schemas directory", '/home/', QFileDialog.ShowDirsOnly)
        self.config_dict['rdf_schemas'] = path
        self.schemaLineEdit.setText(path)
        
    def setSchemaPath(self, configs):
        self.schemaLineEdit.setText(configs.getConfig('rdf_schemas', '') if configs.hasConfig('rdf_schemas') else '')
        
    def getSysDataPath(self):
        path = QFileDialog.getExistingDirectory(self, "Get system dat directory", '/home/', QFileDialog.ShowDirsOnly)
        self.config_dict['sys_data'] = path
        self.sysDataLineEdit.setText(path)
        
    def setSysDataPath(self, configs):
        self.sysDataLineEdit.setText(configs.getConfig('sys_data', '') if configs.hasConfig('sys_data') else '')
