# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 12:45:41 2018

@author: z003umpb
"""
import os

from PyQt5.QtCore import QFileInfo,\
                         QPoint,\
                         QSignalMapper,\
                         QSize,\
                         Qt
                         
from PyQt5.QtGui import QIcon,\
                        QKeySequence
                        
from PyQt5.QtWidgets import QAction,\
                            QApplication,\
                            QFileDialog,\
                            QMainWindow,\
                            QMdiArea,\
                            QMessageBox,\
                            QWidget,\
                            QDockWidget


#from PyQt5.QtCore import pyqtRemoveInputHook
from PyQt5.QtCore import pyqtSignal


from rdfnavigatorsettings         import RDFNavigatorSettings
from rdfnavigatorfind             import RDFNavigatorFind
from rdfnavigatormanagers         import RDFNavigatorSettignsManager, RDFNavigatorResourceReferenceManager

from rdfnavigatorprojectstructure import RDFNavigatorProjectStructure
from rdfnavigatoroutput           import RDFNavigatorOutput
from rdfnavigatorchildren         import RDFNavigatorChildrenTypes
from rdfnavigatorchildrenfactory  import RDFNavigatorChildrenFactory
from rdfnavigatorxmldata          import RDFNavigatorXmlSchema
from rdfnavigatorbookmarks        import RDFNavigatorBookmarks

import rdfnavigator_rc

class RDFNavigator(QMainWindow):
    output_message = pyqtSignal(str)
    def __init__(self):
        super(RDFNavigator, self).__init__()
        
        self.lastDir = '.'
        
        self.settingsManager = RDFNavigatorSettignsManager()
        self.resourceRefManager = RDFNavigatorResourceReferenceManager()
        self.childrenFactory= RDFNavigatorChildrenFactory(self)

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.createDockWidgets()
        self.readSettings()

        self.setWindowTitle("RDF Navigator")
        self.global_data = {}
        
        self.analyzeSystemData()
        #self.setStyleSheet("""QToolTip { background-color: black; color: white; border: black solid 1px }""")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def newFile(self, fileType):
        child = self.createMdiChild(fileType)
        child.newFile()
        child.show()

    def openFileHelper(self, fileName, fileType):
        if fileName:
            self.lastDir = os.path.dirname(fileName)
            existing = self.findMdiChild(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return
            child = self.createMdiChild(fileType)
            child.setManager(self.settingsManager)
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open runntime data format file", self.lastDir, "RDF Files (*.RDF);;XML Files (*.xml)")
        self.openFileHelper(fileName, RDFNavigatorChildrenTypes.XML)
        
    def openProject(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open XML schema project file", self.lastDir, "XML Schema Files (*.xsd);;")
        self.openFileHelper(fileName, RDFNavigatorChildrenTypes.SCHEMA)
        child = self.findMdiChild(fileName)
        if child:
            schema = RDFNavigatorXmlSchema()
            schema.validation_message.connect(self.output_message)
            schema.setSchemaPath(fileName)
            graph = schema.getSchemaDependencyGraph()
            self.projectStructureWidget.createProjectTree(fileName, graph, RDFNavigatorChildrenTypes.SCHEMA)
            self.projectStructureWidget.open_file_request.connect(self.openFileHelper)
            
    def openTemplate(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open system data template file", self.lastDir, "XML Template Files (*.xml);;")
        self.openFileHelper(fileName, RDFNavigatorChildrenTypes.TEMPLATE)
        child = self.findMdiChild(fileName)
        if child:
            schema = RDFNavigatorXmlSchema()
            schema.validation_message.connect(self.output_message)
            schema.setSchemaPath(fileName)
            graph = schema.getTemplateDependencyGraph()
            self.projectStructureWidget.createProjectTree(fileName, graph, RDFNavigatorChildrenTypes.TEMPLATE)
            self.projectStructureWidget.createObjectsTree(fileName)
            self.projectStructureWidget.createFileSystemTree(fileName)
            self.projectStructureWidget.open_file_request.connect(self.openFileHelper)

    def save(self):
        if self.activeMdiChild() and self.activeMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def cut(self):
        if self.activeMdiChild():
            self.activeMdiChild().cut()

    def copy(self):
        if self.activeMdiChild():
            self.activeMdiChild().copy()

    def paste(self):
        if self.activeMdiChild():
            self.activeMdiChild().paste()
    
    def activateFind(self):
        child = self.activeMdiChild()
        find = RDFNavigatorFind(self)
        
        find.findAllCurrentClicked.connect(child.findAll)
        find.findNextClicked.connect(child.findNextWord)
        find.findCountClicked.connect(child.countWord)
        
        if child.hasSelectedText():
            text = child.selectedText()
            find.setFindText(text)
        find.show()

    def about(self):
        QMessageBox.about(self, "About RDF Navigator", "Tool to simplify work with RDF data")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.saveAct.setEnabled(hasMdiChild)
        self.saveAsAct.setEnabled(hasMdiChild)
        self.pasteAct.setEnabled(hasMdiChild)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

        hasSelection = (self.activeMdiChild() is not None and self.activeMdiChild().hasSelectedText())
        
        self.cutAct.setEnabled(hasSelection)
        self.copyAct.setEnabled(hasSelection)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createMdiChild(self, childType):
        child = self.childrenFactory.createObject(childType)
        self.mdiArea.addSubWindow(child)
        child.copyAvailable.connect(self.cutAct.setEnabled)
        child.copyAvailable.connect(self.copyAct.setEnabled)
        return child

    def createActions(self):
        self.newAct         =     QAction(QIcon(':/images/new.png'), "&New", self, shortcut=QKeySequence.New, statusTip="Create a new file", triggered=self.newFile)
        self.openFileAct    = QAction(QIcon(':/images/open.png'), "&Open file...", self, shortcut=QKeySequence.Open, statusTip="Open an existing file", triggered=self.open)
        self.openProjectAct = QAction(QIcon(':/images/openProject.png'), "&Open project...", self, shortcut=QKeySequence("Ctrl+Shift+O"), statusTip="Open an existing project", triggered=self.openProject)
        self.openTemplate   = QAction(QIcon(':/images/sdt.png'), "&Open template...", self, shortcut=QKeySequence("Alt+Shift+O"), statusTip="Open an existing template", triggered=self.openTemplate)
        self.saveAct        = QAction(QIcon(':/images/save.png'), "&Save", self, shortcut=QKeySequence.Save, statusTip="Save the document to disk", triggered=self.save) 
        self.saveAsAct      = QAction("Save &As...", self, shortcut=QKeySequence.SaveAs, statusTip="Save the document under a new name", triggered=self.saveAs) 
        self.exitAct        = QAction("E&xit", self, shortcut=QKeySequence.Quit, statusTip="Exit the application", triggered=QApplication.instance().closeAllWindows)
        
        self.cutAct =      QAction(QIcon(':/images/cut.png'), "Cu&t", self, shortcut=QKeySequence.Cut, statusTip="Cut the current selection's contents to the clipboard", triggered=self.cut)
        self.copyAct =     QAction(QIcon(':/images/copy.png'), "&Copy", self, shortcut=QKeySequence.Copy, statusTip="Copy the current selection's contents to the clipboard", triggered=self.copy)
        self.pasteAct =    QAction(QIcon(':/images/paste.png'), "&Paste", self, shortcut=QKeySequence.Paste, statusTip="Paste the clipboard's contents into the current selection", triggered=self.paste)
        self.findAct =     QAction(QIcon(':/images/find.png'), "&Find", self, shortcut=QKeySequence.Find, statusTip="Find text", triggered=self.activateFind)
        
        self.settingsAct = QAction(QIcon(':/images/settings.png'), "Open settings", self, shortcut=QKeySequence("Ctrl+1"), statusTip="Open Settings", triggered=self.activateSettings)

        self.showProjectStructAct = QAction(QIcon(':/images/project_structure.png'), "Show structure", self, shortcut=QKeySequence("Alt+1"), statusTip="Show project structure", triggered=self.showProjectStructure)
        self.showOutputAct = QAction(QIcon(':/images/project_output.png'), "Show output", self, shortcut=QKeySequence("Alt+2"), statusTip="Show output", triggered=self.showOutput)
        self.showBookmarks = QAction(QIcon(':/images/project_bookmarks.png'), "Show bookmarks", self, shortcut=QKeySequence("Alt+3"), statusTip="Show bookmarks", triggered=self.showBookmarks)

        self.closeAct =    QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.closeAllAct = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.tileAct =     QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.cascadeAct =  QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.nextAct =     QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.previousAct = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct =   QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, statusTip="Show the Qt library's About box", triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openFileAct)
        self.fileMenu.addAction(self.openProjectAct)
        self.fileMenu.addAction(self.openTemplate)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        action = self.fileMenu.addAction("Switch layout direction")
        action.triggered.connect(self.switchLayoutDirection)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addAction(self.findAct)

        self.settingsMenu = self.menuBar().addMenu("Set&tings")
        self.settingsMenu.addAction(self.settingsAct)

        self.viewMenu = self.menuBar().addMenu("&View")
        self.createViewMenu()
        
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openFileAct)
        self.fileToolBar.addAction(self.openProjectAct)
        self.fileToolBar.addAction(self.openTemplate)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWidgets(self):
        self.projectStructureWidget = RDFNavigatorProjectStructure(self)
        self.projectStructureDockWidget = QDockWidget("Project structure", self)
        self.projectStructureDockWidget.setWidget(self.projectStructureWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.projectStructureDockWidget)
        
        
        self.projectOutputWidget = RDFNavigatorOutput(self)
        self.projectOutputDockWidget = QDockWidget("Project output", self)
        self.projectOutputDockWidget.setWidget(self.projectOutputWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.projectOutputDockWidget)
        
        self.output_message.connect(self.projectOutputWidget.write)
        
        self.bookmarskWidget = RDFNavigatorBookmarks(self)
        self.bookmarksDockWidget = QDockWidget("Bookmarks", self)
        self.bookmarksDockWidget.setWidget(self.bookmarskWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bookmarksDockWidget)
        self.bookmarskWidget.bookmark_ref_requested.connect(self.showBookmark)

    def readSettings(self):
        pos = self.settingsManager.getConfig('pos', QPoint(200, 200))
        size = self.settingsManager.getConfig('size', QSize(400, 400))
        self.lastDir = self.settingsManager.getConfig('lastDir', '')
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        self.settingsManager.setConfig('pos', self.pos())
        self.settingsManager.setConfig('size', self.size())
        self.settingsManager.setConfig('lastDir', self.lastDir)

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def switchLayoutDirection(self):
        if self.layoutDirection() == Qt.LeftToRight:
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)
   
    
    def activateSettings(self):
        settingsDlg = RDFNavigatorSettings(self)
        
        settingsDlg.setPluginsPath(self.settingsManager)
        settingsDlg.setRDFToolsPath(self.settingsManager)
        settingsDlg.setSchemaPath(self.settingsManager)
        settingsDlg.setSysDataPath(self.settingsManager)
        
        settingsDlg.exec_()
        settingsDict = settingsDlg.getConfig()
        map(lambda (x, y): self.settingsManager.setConfig(x, y), settingsDict.items())
        
    def analyzeSystemData(self):
        self.resourceRefManager.setSysDataPath(self.settingsManager.getConfig('sys_data', ''))
        self.refs_data, self.vals_data = self.resourceRefManager.analyzeRefs()
        
        self.file_refs_data = dict(reduce(lambda x, y: x + y, [[(v, keys) for v in vals]  for keys, vals in self.refs_data.iteritems() if vals != {}]))

    def showReference(self, obj_name, key_id):
        child_name = self.file_refs_data[obj_name]
        child = self.findMdiChild(child_name)
        if child is None:
            self.openFileHelper(child_name, RDFNavigatorChildrenTypes.TEMPLATE)
            child = self.findMdiChild(child_name)
        self.mdiArea.setActiveSubWindow(child)
        line = self.refs_data[child_name][obj_name][key_id]
        child.widget().goToLine(line)

    def showReferenceValue(self, obj_name, key_id):
        child_name = self.file_refs_data[obj_name]
        value = self.vals_data[child_name][obj_name][key_id]
        child = self.activeMdiChild()
        if child is not None:
            child.displayRefValue(value)

    def showBookmark(self, filename, line):
        child = self.findMdiChild(filename)
        if child is None:
            self.openFileHelper(filename, RDFNavigatorChildrenTypes.TEMPLATE)
            child = self.findMdiChild(filename)
        self.mdiArea.setActiveSubWindow(child)
        child.widget().goToLine(line)

    def createViewMenu(self):
        self.viewMenu.addAction(self.showProjectStructAct)
        self.viewMenu.addAction(self.showOutputAct)
        self.viewMenu.addAction(self.showBookmarks)

    def showProjectStructure(self):
        self.projectStructureDockWidget.show()

    def showOutput(self):
        self.projectOutputDockWidget.show()

    def showBookmarks(self):
        self.bookmarksDockWidget.show()

