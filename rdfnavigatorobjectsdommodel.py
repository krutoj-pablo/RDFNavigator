# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:42:49 2018

@author: z003umpb
"""
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QIcon

class RDFNavigatorObjectsDomItem(object):
    def __init__(self, node, row, parent=None):
        self.domNode = node
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = {}

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentItem

    def child(self, i):
        if i in self.childItems:
            return self.childItems[i]
        if i >= 0 and i < self.domNode.attributes().count():
            childNode = self.domNode.attributes().item(i)
            childItem = RDFNavigatorObjectsDomItem(childNode, i, self)
            self.childItems[i] = childItem
            return childItem
        elif i >= self.domNode.attributes().count() and i < (self.domNode.childNodes().count() + self.domNode.attributes().count()):
            childNode = self.domNode.childNodes().item(i - self.domNode.attributes().count())
            childItem = RDFNavigatorObjectsDomItem(childNode, i, self)
            self.childItems[i] = childItem
            return childItem
        return None

    def row(self):
        return self.rowNumber

class RDFNavigatorObjectsDomModel(QAbstractItemModel):
    def __init__(self, document, parent=None):
        super(RDFNavigatorObjectsDomModel, self).__init__(parent)
        
        self.domDocument = document
        self.rootItem = RDFNavigatorObjectsDomItem(self.domDocument, 0)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            item = index.internalPointer()
            node = item.node()
            if index.column() == 0:
                if node.isText():
                    return node.nodeValue()
                return node.nodeName()
        if role == Qt.DecorationRole:
            item = index.internalPointer()
            node = item.node()
            if node.isAttr():
                return QIcon(':/images/xml_property.png')
            if node.isElement():
                return QIcon(':/images/xml_node.png')
            if node.isText():
                return QIcon(':/images/xml_text.png')
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "Objects Tree"
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()
        childItem = child.internalPointer()
        parentItem = childItem.parent()
        if not parentItem or parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        nodes = parentItem.node().childNodes().count()
        attributes = parentItem.node().attributes().count()
        return  nodes + attributes