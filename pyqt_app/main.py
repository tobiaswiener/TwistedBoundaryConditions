# -*- coding: utf-8 -*-
"""
Example demonstrating a variety of scatter plot features.
"""
import sys

from PyQt6 import QtGui, QtCore, QtWidgets

from collections import namedtuple
from itertools import chain
from mainWidget import MainWidget




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # app = pg.mkQApp("Scatter Plot Item Example")
    mw = MainWindow()

    mw.show()
    sys.exit(app.exec())

