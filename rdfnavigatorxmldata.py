# -*- coding: utf-8 -*-
"""
Created on Fri Mar 02 15:26:46 2018

@author: z003umpb
"""

import lxml
import os

from collections import defaultdict
from lxml import etree
from lxml.etree import DocumentInvalid

from PyQt5.QtCore import pyqtSignal, QObject

class RDFNavigatorSingleFileScanner(object):
    def __init__(self, *args, **kwargs):
        self.fileName = kwargs.get('fileName', None)
        self.references = {}

    def analyze(self, *args, **kwargs):
        with open(self.fileName, 'r') as f:
            doc = etree.parse(f)
        root  = doc.getroot()
        for elem in root.getiterator():
            if not hasattr(elem.tag, 'find'): continue
            i = elem.tag.find('}')
            if i >= 0:
                elem.tag = elem.tag[i + 1:]
        return self.__analyzeTextLibraries(root=root)
        
    
    def __analyzeTextLibraries(self, *args, **kwargs):
        tagName = 'TextLibraries'
        root = kwargs.get('root', None)
        if root is None:
            return
        libs = root.find(tagName)
        refs, vals = {}, {}
        if libs is not None:
            for lib in filter(lambda x: type(x.tag) == str, libs.getchildren()):
                refs[lib.attrib['Name']] = dict([(x.attrib['ID'], x.sourceline) for x in lib.getchildren() if type(x.tag) == str and x.attrib.has_key('ID')])
                vals[lib.attrib['Name']] = dict([(x.attrib['ID'], x.text) for x in lib.getchildren() if type(x.tag) == str and x.attrib.has_key('ID')])
        return refs, vals


        

class RDFNavigatorCrossFileScanner(object):
    pass

class RDFNavigatorTablesList(object):
   def __init__(self):
       pass

class RDFNavigatorXmlSchema(QObject):
    validation_message = pyqtSignal(str)
    def __init__(self, parent=None):
        self.mainPath = None
        super(RDFNavigatorXmlSchema, self).__init__(parent)
        
    def setSchemaPath(self, path):
        self.path = path

    def validateSchema(self):
        pass

    def getDependencyGraph(self, refAttr):
        graph = defaultdict(lambda: [])
        def scanHelper(path, graph):
            if graph.has_key(path):
                return graph
            self.validation_message.emit("Scanning file: {0}".format(path))
            with open(path, 'r') as f:
                doc = etree.parse(f)
            root  = doc.getroot()
            for elem in root.getiterator():
                if not hasattr(elem.tag, 'find'): continue
                i = elem.tag.find('}')
                if i >= 0:
                    elem.tag = elem.tag[i + 1:]
            items =  [t.attrib[refAttr] for t in root.getchildren() if t.tag == 'include' ]
            graph[path] = items
            map(lambda x: scanHelper(os.path.join(os.path.dirname(path), x), graph), items)
            return graph
        return scanHelper(self.path, graph)

    
    def getSchemaDependencyGraph(self):
        return self.getDependencyGraph('schemaLocation')

    def getTemplateDependencyGraph(self):
        return self.getDependencyGraph('href')
    
    def validateDocument(self, text):
        with open(self.path, 'r') as f:
            doc = etree.parse(f)
        self.validation_message.emit("Validating root schema ... ")
        try:
            schema = etree.XMLSchema(doc)
        except lxml.etree.XMLSchemaParseError as e:
            self.validation_message.emit("Root schema validation failed ... {0}".format(e.message))
            return
        self.validation_message.emit("Root schema validated ... OK")
        try:
            self.validation_message.emit("Validating XML file ...")
            xmldoc = etree.fromstring(text.decode('utf-8').encode('ascii'))
            schema.assertValid(xmldoc)
        except  DocumentInvalid as e:
            self.validation_message.emit("Validating XML file failed ... {0}".format(e.message))
        self.validation_message.emit("Validating XML file ... OK")
