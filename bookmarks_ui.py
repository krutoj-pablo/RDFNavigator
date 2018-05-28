# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\bookmarks.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookmarksWidget(object):
    def setupUi(self, BookmarksWidget):
        BookmarksWidget.setObjectName("BookmarksWidget")
        BookmarksWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(BookmarksWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bookmarksTabWidget = QtWidgets.QTabWidget(BookmarksWidget)
        self.bookmarksTabWidget.setObjectName("bookmarksTabWidget")
        self.bookmarks = QtWidgets.QWidget()
        self.bookmarks.setObjectName("bookmarks")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.bookmarks)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bookmarksWidget = QtWidgets.QTableWidget(self.bookmarks)
        self.bookmarksWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.bookmarksWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.bookmarksWidget.setGridStyle(QtCore.Qt.DashLine)
        self.bookmarksWidget.setObjectName("bookmarksWidget")
        self.bookmarksWidget.setColumnCount(3)
        self.bookmarksWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.bookmarksWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.bookmarksWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.bookmarksWidget.setHorizontalHeaderItem(2, item)
        self.bookmarksWidget.horizontalHeader().setVisible(True)
        self.bookmarksWidget.verticalHeader().setVisible(False)
        self.bookmarksWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.bookmarksWidget)
        self.bookmarksTabWidget.addTab(self.bookmarks, "")
        self.verticalLayout.addWidget(self.bookmarksTabWidget)

        self.retranslateUi(BookmarksWidget)
        self.bookmarksTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(BookmarksWidget)

    def retranslateUi(self, BookmarksWidget):
        _translate = QtCore.QCoreApplication.translate
        BookmarksWidget.setWindowTitle(_translate("BookmarksWidget", "Form"))
        self.bookmarksWidget.setSortingEnabled(True)
        item = self.bookmarksWidget.horizontalHeaderItem(0)
        item.setText(_translate("BookmarksWidget", "Fille"))
        item = self.bookmarksWidget.horizontalHeaderItem(1)
        item.setText(_translate("BookmarksWidget", "Line"))
        item = self.bookmarksWidget.horizontalHeaderItem(2)
        item.setText(_translate("BookmarksWidget", "Text"))
        self.bookmarksTabWidget.setTabText(self.bookmarksTabWidget.indexOf(self.bookmarks), _translate("BookmarksWidget", "Bookmarks"))

