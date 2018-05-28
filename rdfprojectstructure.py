# -*- coding: utf-8 -*-
"""
Created on Wed May 02 14:01:04 2018

@author: z003umpb
"""

from projectstructure_ui import Ui_ProjectStructureWidget

class RDFNavigatorProjectStructure(QtWidgets.QDialog, Ui_ProjectStructureWidget):
    
    def __init__(self, parent=None):
        super(RDFNavigatorProjectStructure, self).__init__(parent)
        self.setupUi(self)
