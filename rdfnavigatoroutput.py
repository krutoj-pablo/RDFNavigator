# -*- coding: utf-8 -*-
"""
Created on Wed May 02 15:16:35 2018

@author: z003umpb
"""
from PyQt5.QtWidgets import QWidget

from output_ui import Ui_ProjectOutputWidget

class RDFNavigatorOutput(QWidget, Ui_ProjectOutputWidget):
    
    def __init__(self, parent=None):
        super(RDFNavigatorOutput, self).__init__(parent)
        self.setupUi(self)

    def write(self, text):
        self.textEdit.append("<b>{0}</b>".format(text))