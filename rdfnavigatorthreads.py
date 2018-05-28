# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 12:35:27 2018

@author: z003umpb
"""
import os
import subprocess

from PyQt5.QtCore import QThread, pyqtSignal

class RDFNavigatorTransformThread(QThread):
    rdf2xml_transform_done = pyqtSignal(str)
    xml2rdf_transform_done = pyqtSignal(str, str)
    
    def __init__(self, **kwargs):
        self.fileName     = kwargs.get('fileName', None)
        self.direction    = kwargs.get('direction', None)
        self.rdf_tools    = kwargs.get('rdf_tools', None)
        self.rdf_plugins  = kwargs.get('rdf_plugins', None)
        self.origFileName = kwargs.get('orig_file_name', None)
        QThread.__init__(self)
        
    def __del__(self):
        self.wait()

    def do_transformation(self):
        cmd = [os.path.join(self.rdf_tools, self.direction), self.fileName, '-plugins:{0}'.format(self.rdf_plugins)]
        cmd = map(lambda x: x.replace('/', '\\'), cmd)
        
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        print out, err
        
        transform_from, transform_to = self.direction.split('2')
        new_name = os.path.join(os.path.dirname(self.fileName), os.path.basename(self.fileName).replace(".{0}".format(transform_from), '.{0}'.format(transform_to)))

        if os.path.isfile(new_name):
            return new_name
        return None

    def run(self):
        if all([self.fileName, self.direction, self.rdf_tools, self.rdf_plugins]) :
            new_name = self.do_transformation()
            if self.direction == 'rdf2xml' and new_name is not None:
                self.rdf2xml_transform_done.emit(new_name)
            if self.direction == 'xml2rdf' and new_name is not None:
                self.xml2rdf_transform_done.emit(self.origFileName, new_name)
        
        