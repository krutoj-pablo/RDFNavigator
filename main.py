# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from rdfnavigator import RDFNavigator

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/images/navigator.png'))
    rdf_navigator = RDFNavigator()
    rdf_navigator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()