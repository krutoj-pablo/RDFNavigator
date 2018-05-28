# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:01:46 2018

@author: z003umpb
"""
import os

from abc import ABCMeta

from multiprocessing import Pool, cpu_count

from PyQt5.QtCore import QSettings

from rdfnavigatorxmldata import RDFNavigatorSingleFileScanner

def scanSingleFileHelper(fileName):
    scanner = RDFNavigatorSingleFileScanner(fileName=fileName)
    return fileName, scanner.analyze()

class RDFNavigatorManagerBase:
    __metaclass__ = ABCMeta

    def __str__(self):
        pass

class RDFNavigatorSettignsManager(RDFNavigatorManagerBase):
    def __init__(self, parent=None):
        self.config = QSettings('Siemens', 'RDFNavigator')

    def __str__(self):
        return str(self.__class__)

    def getConfig(self, key, valueType):
        return self.config.value(key, valueType)

    def setConfig(self, key, value):
        self.config.setValue(key, value)

    def getConfigs(self):
        return self.config

    def hasConfig(self, key):
        return self.config.contains(key)

class RDFNavigatorResourceReferenceManager(RDFNavigatorManagerBase):
    def __init__(self, parent=None):
        self.parent = parent
        self.sysdatapath = "";

    def setSysDataPath(self, dataPath):
        self.sysdatapath = dataPath

    def getSysDataPath(self, dataPath):
        return self.sysdatapath

    def analyzeRefs(self):
        refs, vals = {}, {}
        pool = Pool(cpu_count())
        
        for result in pool.imap(scanSingleFileHelper, map(lambda x: os.path.join(self.sysdatapath, x), os.listdir(self.sysdatapath))):
            fileName, (r, v ) = result
            refs[fileName], vals[fileName] =  r, v
            print "Fille {0} analyzed".format(fileName)
            
        return refs, vals
