


from PyQt6 import QtWidgets, QtCore

import sys

from collections.abc import Iterable

from pyqt_app.ParameterDicts import *



class ImpListWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QGridLayout()
        self.listWidget = QtWidgets.QListWidget()
        self.btn_delete = QtWidgets.QPushButton("delete")

        self.list = []
        for x in range(5):
            for y in range(6):
                item = ImpInfoWidget(x,y,x+y)
                self.list.append(item)
                self.listWidget.addItem(item)

        self.setupUI()



    def setupUI(self):
        self._layout.addWidget(self.listWidget)
        self._layout.addWidget(self.btn_delete)

        self.btn_delete.clicked.connect(self._delete_imp)

        self.setLayout(self._layout)

    def add_imp(self):
        pass

    def _delete_imp(self):
        imps = self.listWidget.selectedItems()
        for imp in imps:
            ix = self.listWidget.indexFromItem(imp)
            self.listWidget.takeItem(ix.row())


class ImpInfoWidget(QtWidgets.QListWidgetItem):
    def __init__(self, x, y, energy):
        super().__init__()
        self.x = x
        self.y = y
        self.energy = energy

        self.setText(f"e_imp = {energy} at ({x},{y})")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = ImpListWidget()
    widget.show()
    sys.exit(app.exec())
