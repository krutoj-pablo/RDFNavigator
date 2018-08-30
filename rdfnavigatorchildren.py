# -*- coding: utf-8 -*-
"""
Created on Mon May 14 13:50:31 2018

@author: z003umpb
"""
import tempfile
import os

from PyQt5.QtCore import QFile,\
                         QFileInfo,\
                         QTextStream,\
                         Qt,\
                         pyqtSignal

from PyQt5.QtGui import QIcon
                        
from PyQt5.QtWidgets import QApplication,\
                            QFileDialog,\
                            QMessageBox

from rdfxmleditor import RDFXmlEditor, RDFXmlTemplateEditor
from rdfnavigatorxmldata  import RDFNavigatorXmlSchema
from rdfnavigatorthreads  import RDFNavigatorTransformThread


class RDFNavigatorChildrenTypes(object):
    RDF, XML, SCHEMA, TEMPLATE = range(0, 4)


class RDFNavigatorChildBase(object):

    def newFile(self):
        pass

    def loadFile(self, fileName):
        pass

    def setManager(self, manager):
        self.manager = manager

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        return True

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.isModified())

    def maybeSave(self):
        if self.isModified():
            ret = QMessageBox.warning(self, "RDF Navigator", "'%s' has been modified.\nDo you want to save your changes?" % self.userFriendlyCurrentFile(), QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.save()
            if ret == QMessageBox.Cancel:
                return False
        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()


class RDFNavigatorXmlChild(RDFXmlEditor, RDFNavigatorChildBase):
    sequenceNumber = 1
    output_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super(RDFNavigatorXmlChild, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(QIcon(':/images/xml.png'))
        self.isUntitled = True
        self.isRdf = False
        self.isSchema = False
        self.parent = parent

    def newFile(self):
        self.isUntitled = True
        self.curFile = "document%d.xml" % RDFNavigatorXmlChild.sequenceNumber
        RDFNavigatorXmlChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')
        self.textChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        if fileName.endswith('.xml'):
            self.isRdf = False
            self.loadXml(fileName)
        elif fileName.endswith('.rdf'):
            self.isRdf = True
            self.loadRdf(fileName)
        elif fileName.endswith('.xsd'):
            self.isRdf = False
            self.loadXsd(fileName)
        return True

    def saveFile(self, fileName):
        if self.isRdf:
            self.saveRdf(fileName)
        else:
            self.saveXml(fileName)
        return True

    def loadXml(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "RDFNavigator", "Cannot read file {0}:\n{1}.".format(fileName, file.errorString()))
            return False
        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setText(instr.readAll())
        self.indicateUlrs()
        QApplication.restoreOverrideCursor()
        if self.isRdf:
            fileName = fileName.replace('.xml', '.rdf')
        self.setCurrentFile(fileName)
        self.textChanged.connect(self.documentWasModified)

    def loadXsd(self, fileName):
        self.isSchema = True
        self.loadXml(fileName)

    def loadRdf(self, fileName):
        tools = self.manager.getConfig('rdf_tools', '')
        plugins = self.manager.getConfig('rdf_plugins', '')
        thread = RDFNavigatorTransformThread(fileName=fileName, direction='rdf2xml', rdf_tools=tools, rdf_plugins=plugins)
        thread.rdf2xml_transform_done.connect(self.loadXml)
        thread.transform_output.connect(self.output_message)
        thread.run()

    def saveRdf(self, fileName):
        fd, tempFile = tempfile.mkstemp(suffix='.xml', prefix='temp')
        os.close(fd)
        self.saveXml(tempFile)
        self.setCurrentFile(fileName)
        tools = self.manager.getConfig('rdf_tools', '')
        plugins = self.manager.getConfig('rdf_plugins', '')
        thread = RDFNavigatorTransformThread(fileName=tempFile, orig_file_name=fileName, direction='xml2rdf', rdf_tools=tools, rdf_plugins=plugins)
        thread.rdf2xml_transform_done.connect(self.postSaveRdf)
        thread.run()

    def postSaveRdf(self, originalFileName, fileName):
        os.rename(fileName, originalFileName)

    def saveXml(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "RDF Navigator",  "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False
        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.text()
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)


    def validateDocument(self):
        """TODO: Source schema needs to be attached """
        schemaPath = self.manager.getConfig('rdf_schemas', '')
        schema = RDFNavigatorXmlSchema()
        schema.validation_message.connect(self.parent.output_message)
        schema.setSchemaPath(os.path.join(schemaPath, 'RdfMain.xsd'))
        schema.validateDocument(self.text())

    def contextMenuEvent(self, e):
        menu = self.createBasicContextMenu()
        validateDocAction = menu.addAction("Validate document", self.validateDocument)
        action = menu.exec_(self.mapToGlobal(e.pos()))

class RDFNavigatorSchemaChild(RDFNavigatorXmlChild):
    def __init__(self, parent=None):
        super(RDFNavigatorSchemaChild, self).__init__(parent)


class RDFNavigatorTemplateChild(RDFXmlTemplateEditor, RDFNavigatorChildBase):
    sequenceNumber = 1

    bookmark_added = pyqtSignal(str, int, str)
    bookmark_deleted = pyqtSignal(str, int, str)

    def __init__(self, parent=None):
        super(RDFNavigatorTemplateChild, self).__init__(parent)
        self.marker_added.connect(self.createBookmark)
        self.marker_deleted.connect(self.deleteBookmark)

    def newFile(self):
        self.isUntitled = True
        self.curFile = "template%d.xml" % RDFNavigatorTemplateChild.sequenceNumber
        RDFNavigatorTemplateChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')
        self.textChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        self.loadTemplate(fileName)
        return True

    def saveFile(self, fileName):
        self.saveTemplate(fileName)

    def loadTemplate(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "RDFNavigator", "Cannot read temlate file {0}:\n{1}.".format(fileName, file.errorString()))
            return False
        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setText(instr.readAll())
        self.indicateAll()
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)

    def saveTemplate(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "RDF Navigator",  "Cannot write template file %s:\n%s." % (fileName, file.errorString()))
            return False
        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.text()
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)

    def createBookmark(self, line):
        data = self.text(line)
        self.bookmark_added.emit(self.curFile, line, data)

    def deleteBookmark(self, line):
        data = self.text(line)
        self.bookmark_deleted.emit(self.curFile, line, data)