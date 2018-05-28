# -*- coding: utf-8 -*-
"""
Created on Thu Mar 01 17:09:26 2018

@author: z003umpb
"""

from PyQt5 import QtWidgets

from find_ui import Ui_FindDialog
from PyQt5.QtCore import Qt, pyqtSignal

class RDFNavigatorFind(QtWidgets.QDialog, Ui_FindDialog):
    findAllCurrentClicked = pyqtSignal(str, bool, bool, bool, bool)
    findCountClicked      = pyqtSignal(str, bool, bool)
    findNextClicked       = pyqtSignal(str, bool, bool, bool, bool, bool)

    def __init__(self, parent=None):
        super(RDFNavigatorFind, self).__init__(parent)
        self.setupUi(self)
        self.isRe, self.matchCase, self.wrapAround, self.wordOnly, self.backDirection = False, False, False, False, True
         
        self.findAllInCurPushButton.clicked.connect(self.findAllCurrent)
        self.findPushButton.clicked.connect(self.findNext)

        self.backDirectionBox.stateChanged.connect(self.setBackDirection)
        self.matchWordBox.stateChanged.connect(self.setMatchWord)
        self.matchCaseBox.stateChanged.connect(self.setMatchCase)
        self.wrapAroundBox.stateChanged.connect(self.setWrapAround)

        self.reRadioButton.toggled.connect(self.setRe)

    def setFindText(self, text):
        self.findLineEdit.setText(text)

    def findAllCurrent(self):
        self.findAllCurrentClicked.emit(self.findLineEdit.text(), self.isRe, self.matchCase, self.wordOnly, self.backDirection)

    def findCount(self):
        self.findCountClicked.emit(self.findLineEdit.text(), self.isRe, self.matchCase)

    def findNext(self):
        self.findNextClicked.emit(self.findLineEdit.text(), self.isRe, self.matchCase, self.wrapAround, self.wordOnly, self.backDirection)

    def setBackDirection(self, val):
        self.backDirection = val != Qt.Checked

    def setMatchWord(self, val):
        self.wordOnly = val == Qt.Checked

    def setMatchCase(self, val):
        self.matchCase = val == Qt.Checked

    def setWrapAround(self, val):
        self.wrapAround = val == Qt.Checked

    def setRe(self, val):
        self.isRe = val
