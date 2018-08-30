# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:03:28 2018

@author: z003umpb
"""
import re

from PyQt5.QtGui import QFont, QFontMetrics, QColor, QKeySequence
from PyQt5.QtWidgets import QToolTip
from PyQt5.Qsci import QsciScintilla, QsciLexerXML, QsciAPIs

from PyQt5.QtCore import Qt, pyqtRemoveInputHook
from PyQt5.QtCore import pyqtSignal, QPoint

from PyQt5.QtWidgets import QMenu

class RDFXmlEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8
    INDICATOR_URL = 9

    marker_added = pyqtSignal(int)
    marker_deleted = pyqtSignal(int)

    def __init__(self, parent=None):
        super(RDFXmlEditor, self).__init__(parent)
        self.parent = parent
        self.indicatorDefine(QsciScintilla.PlainIndicator, self.INDICATOR_URL)


        self.setCaretLineVisible(True)
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)
        
        # Set the default font
        font = QFont()
        font.setFamily('Courier New')
        font.setFixedPitch(True)
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.reactOnMarginClicked)
            
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)

        self.setMarginSensitivity(2, True)
        self.setMarginType(2, QsciScintilla.SymbolMargin )
        self.setFolding(QsciScintilla.CircledTreeFoldStyle,2)
        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setIndentationGuides(True)
        # Current line visible with special background color
        
        self.setWrapMode(QsciScintilla.WrapWhitespace)
        
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        self.lexer = QsciLexerXML()

        self.lexer.setDefaultFont(font)
        self.lexer.setColor(QColor(26, 26, 255, 250), QsciLexerXML.Tag)
        font = self.lexer.font(QsciLexerXML.Tag)
        font.setBold(True)
        self.lexer.setFont(font, QsciLexerXML.Tag)
        
        self.lexer.setColor(QColor(230, 115, 0, 250), QsciLexerXML.Attribute)
        font = self.lexer.font(QsciLexerXML.Attribute)
        font.setBold(True)
        self.lexer.setFont(font, QsciLexerXML.Attribute)
        
        self.lexer.setColor(QColor(0, 148, 43, 250), QsciLexerXML.HTMLDoubleQuotedString)
        font = self.lexer.font(QsciLexerXML.HTMLDoubleQuotedString)
        font.setBold(True)
        self.lexer.setFont(font, QsciLexerXML.HTMLDoubleQuotedString)
        #lexer.setColor(QColor(0, 153, 51, 250), QsciLexerXML.XMLStart)
        #lexer.setColor(QColor(0, 153, 51, 250), QsciLexerXML.XMLEnd)
        self.setLexer(self.lexer)
        #self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(600, 450)
        self.prevFind = []
        self.firstFindDone = False
    
    def createBasicContextMenu(self):
        contextMenu = QMenu(self)
        undoAction = contextMenu.addAction("Undo", self.undo, QKeySequence.Undo)
        redoAction = contextMenu.addAction("Redo", self.redo, QKeySequence.Redo)
        
        cutAction    = contextMenu.addAction("Cut", self.cut, shortcut=QKeySequence.Cut)
        unduRedoSep  = contextMenu.insertSeparator(cutAction)
        copyAction   = contextMenu.addAction("Copy", self.copy, shortcut=QKeySequence.Copy)
        pasteAction  = contextMenu.addAction("Paste", self.paste, shortcut=QKeySequence.Paste)
        deleteAction = contextMenu.addAction("Delete", self.removeSelectedText, QKeySequence.Delete)

        selectAllAction = contextMenu.addAction("SelectAll", self.selectAll, QKeySequence.SelectAll)
        editSeparator = contextMenu.insertSeparator(selectAllAction)
        return contextMenu


    def reactOnMarginClicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
            self.marker_deleted.emit(nline)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
            self.marker_added.emit(nline)

    def indicateUlrs(self):
        self.indicatorHelper('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.INDICATOR_URL)

    def indicatorHelper(self, re_string, indicator):
        ref_regexp = re.compile(re_string, re.IGNORECASE)
        for match in ref_regexp.finditer(self.text()):
            self.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, indicator)
            self.SendScintilla(QsciScintilla.SCI_SETINDICATORVALUE, indicator)
            self.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, match.start(), match.end() - match.start())
            self.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, 0)

    def findAll(self, text, isRe, matchCase, wordOnly, backDirection):
        map(lambda (line, start, end): self.clearIndicatorRange(line, start, line, end, self.INDICATOR_TEXT),self.prevFind)
        originalLine, originalStart =  self.getCursorPosition()
        self.setCursorPosition(0, 0)
        if self.findFirst(text, isRe, matchCase, wordOnly, False, backDirection):
            while True:
                line, end =  self.getCursorPosition()
                self.fillIndicatorRange(line, end - len(text), line, end, self.INDICATOR_TEXT)
                self.prevFind.append((line, end - len(text), end))
                if not self.findNext() :
                    break
        self.setCursorPosition(originalLine, originalStart)
    
    def findNextWord(self, text, isRe, matchCase, wrapAround, wordOnly, backDirection):
        if not self.firstFindDone:
            self.findFirst(text, isRe, matchCase, wordOnly, wrapAround, backDirection)
        else:
            self.findNext()
        line, end =  self.getCursorPosition()

    def countWord(self, text, isRe, matchCase):
        if isRe:
            print self.text().find(text)
        elif matchCase:
            print self.text().find(text, Qt.CaseSensitive)
        else:
            print self.text().find(text, Qt.CaseInsensitive)

class RDFXmlTemplateEditor(RDFXmlEditor):
    crossRefRequested = pyqtSignal(str, str)
    crossRefValueRequested = pyqtSignal(str, str)
    INDICATOR_REF, INDICATOR_TEXT, INDICATOR_PLACEHOLDER, INDICATOR_PARAMETER  = range(10, 14)

    def __init__(self, parent=None):
        super(RDFXmlTemplateEditor, self).__init__(parent)
        self.indicatorDefine(QsciScintilla.FullBoxIndicator, self.INDICATOR_REF)
        self.setMatchedBraceIndicator(self.INDICATOR_REF)

        self.indicatorDefine(QsciScintilla.StraightBoxIndicator , self.INDICATOR_TEXT)
        self.setIndicatorForegroundColor(QColor(255, 128, 255, 120), self.INDICATOR_TEXT)

        self.indicatorDefine(QsciScintilla.DiagonalIndicator, self.INDICATOR_PLACEHOLDER)
        self.setIndicatorForegroundColor(QColor(255, 153, 230, 120), self.INDICATOR_PLACEHOLDER)
        self.setIndicatorHoverStyle(QsciScintilla.RoundBoxIndicator)

        self.indicatorDefine(QsciScintilla.StraightBoxIndicator , self.INDICATOR_PARAMETER)
        self.setIndicatorForegroundColor(QColor(255, 128, 128, 120), self.INDICATOR_PARAMETER)
        self.indicatorReleased.connect(self.reactOnIndicatorReleased)
        self.cursorPositionChanged.connect(self.reactOnCursorPositionChanged)
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.__prepare_autoCompletion()

    def indicateRefs(self):
        self.indicatorHelper('\{[A-Za-z]+\.[0-9]+\}', self.INDICATOR_REF)

    def indicatePlaceholders(self):
        self.indicatorHelper('\$\$[A-Za-z]+\$\$', self.INDICATOR_PLACEHOLDER)

    def indicateParameters(self):
        self.indicatorHelper('\%\%[A-Za-z].+\%\%', self.INDICATOR_PARAMETER)

    def __parse_ref(self, line, index):
        text = self.text(line) 
        start = index
        end = index
        while text[start] != '{':
            start -= 1
        while text[end] != '}':
            end += 1
        resource, resource_id = text[start + 1:end].split('.')
        return resource, resource_id

    def goToLine(self, line):
        self.SendScintilla(QsciScintilla.SCI_GOTOLINE, line - 1)

    def displayRefValue(self, message):
        line, index = self.getCursorPosition()
        position = self.positionFromLineIndex(line, index)
        x = self.SendScintilla(QsciScintilla.SCI_POINTXFROMPOSITION, 0, position)
        y = self.SendScintilla(QsciScintilla.SCI_POINTYFROMPOSITION, 0, position)
        point = self.mapToGlobal(QPoint(x, y))
        QToolTip.showText(point, unicode("Meaning: {0}").format(message), self)

    def reactOnIndicatorReleased(self, line, index, keys):
        position = self.positionFromLineIndex(line, index)
        value = self.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, self.INDICATOR_REF, position)
        if value != 0:
            resource, resource_id = self.__parse_ref(line, index)
            self.crossRefRequested.emit(resource, resource_id)
            

    def reactOnCursorPositionChanged(self, line, index):
        position = self.positionFromLineIndex(line, index)
        value = self.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, self.INDICATOR_REF, position)
        if value != 0:
            resource, resource_id = self.__parse_ref(line, index)
            self.crossRefValueRequested.emit(resource, resource_id)

    def indicateAll(self):
        self.indicateUlrs()
        self.indicateRefs()
        self.indicatePlaceholders()
        self.indicateParameters()

    def __prepare_autoCompletion(self):
        self.api = QsciAPIs(self.lexer)
        self.setAutoCompletionThreshold(5)
        autocompletions = ["variable_one", "variable_two", "function_one(int arg_1)", "function_two(float arg_1)"]
        map(self.api.add, autocompletions)
        self.api.prepare()

