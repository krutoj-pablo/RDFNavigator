# -*- coding: utf-8 -*-
"""
Created on Wed May 02 15:16:35 2018

@author: z003umpb
"""
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt
from PyQt5.QtCore    import pyqtSignal

from bookmarks_ui import Ui_BookmarksWidget

class RDFNavigatorBookmarks(QWidget, Ui_BookmarksWidget):
    bookmark_ref_requested = pyqtSignal(str, int)
    FILE, LINE, TEXT = range(3)

    def __init__(self, parent=None):
        super(RDFNavigatorBookmarks, self).__init__(parent)
        self.setupUi(self)
        self.bookmarksWidget.itemClicked.connect(self.activateBookmarkItem)

    def addBookmark(self, filename, line, data):
        rowPosition = 0
        
        self.bookmarksWidget.insertRow(rowPosition)
        self.bookmarksWidget.setItem(rowPosition , self.FILE, QTableWidgetItem(QIcon(':/images/bookmark.png'), filename))
        self.bookmarksWidget.setItem(rowPosition , self.LINE, QTableWidgetItem(str(line)))
        self.bookmarksWidget.setItem(rowPosition , self.TEXT, QTableWidgetItem(data))
        self.bookmarksWidget.resizeColumnsToContents()

    def removeBookmark(self, filename, line, data):
        files = self.bookmarksWidget.findItems(filename, Qt.MatchExactly)
        lines = self.bookmarksWidget.findItems(str(line), Qt.MatchExactly)
        datas = self.bookmarksWidget.findItems(data, Qt.MatchExactly)
        lines_to_remove = list(set(map(lambda x: x.row(),files)).intersection(set(map(lambda x: x.row(),lines))).intersection(set(map(lambda x: x.row(), datas))))
        map(self.bookmarksWidget.removeRow, lines_to_remove)


    def activateBookmarkItem(self, item):
        row = item.row()
        filename, line = self.bookmarksWidget.item(row, self.FILE) , self.bookmarksWidget.item(row, self.LINE)
        self.bookmark_ref_requested.emit(filename.text(), int(line.text()) + 1)
