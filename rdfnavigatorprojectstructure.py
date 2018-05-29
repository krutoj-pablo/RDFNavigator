# -*- coding: utf-8 -*-
"""
Created on Wed May 02 14:01:04 2018

@author: z003umpb
"""
import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QFile, QIODevice, pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QFileSystemModel
from PyQt5.QtXml import QDomDocument

#from PyQt5.QtCore import pyqtRemoveInputHook
from rdfnavigatorobjectsdommodel import RDFNavigatorObjectsDomModel

from projectstructure_ui import Ui_ProjectStructureWidget

class RDFNavigatorProjectStructure(QWidget, Ui_ProjectStructureWidget):
    open_file_request = pyqtSignal(str, int)
    def __init__(self, parent=None,):
        super(RDFNavigatorProjectStructure, self).__init__(parent)
        self.setupUi(self)
        self.basicStructureWidget.itemDoubleClicked.connect(self.createOpenFileRequest)
        self.childType = None
        self.objectsStructureModel = RDFNavigatorObjectsDomModel(QDomDocument(), self)
        self.objectsStructureView.setModel(self.objectsStructureModel)

    def createProjectTree(self, fileName, graph, childType):
        def createProjectTreeHelper(fileName, graph, root):
            for i in graph[fileName]:
                item = QTreeWidgetItem(root)
                filePath = os.path.join(os.path.dirname(fileName), i)
                item.setText(0, i)
                item.setData(0, Qt.UserRole, filePath)
                item.setIcon(0, QIcon(':/images/xsd.png'))
                createProjectTreeHelper(filePath, graph, item)
        self.childType =childType
        root = QTreeWidgetItem(self.basicStructureWidget)
        root.setText(0, os.path.basename(fileName))
        root.setData(0, Qt.UserRole, fileName)
        root.setIcon(0, QIcon(':/images/xsd.png'))
        createProjectTreeHelper(fileName, graph, root)

    def createOpenFileRequest(self, item, column):
        self.open_file_request.emit(item.data(0, Qt.UserRole), self.childType)

    def createObjectsTree(self, filePath):
        if os.path.exists(filePath):
            f = QFile(filePath)
            if f.open(QIODevice.ReadOnly):
                document = QDomDocument()
                if document.setContent(f):
                    newModel = RDFNavigatorObjectsDomModel(document, self)
                    self.objectsStructureView.setModel(newModel)
                    self.objectsStructureModel = newModel
                f.close()

    def createFileSystemTree(self, filePath):
        self.filesystemModel = QFileSystemModel(self)
        self.filesystemModel.setRootPath(os.path.dirname(filePath))
        self.filesystemTreeView.setModel(self.filesystemModel)
        map(self.filesystemTreeView.hideColumn, range(1, 4))

    def on_filesystemTreeView_doubleClicked(self, index):
        file_path = self.filesystemModel.filePath(index)
        self.open_file_request.emit(file_path, self.childType)