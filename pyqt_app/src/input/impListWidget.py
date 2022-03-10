
from PyQt6 import QtWidgets, QtCore

import sys



class ImpListWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._layout = QtWidgets.QGridLayout()
        self.listWidget = QtWidgets.QListWidget()
        self.btn_delete = QtWidgets.QPushButton("delete")
        self.btn_clear = QtWidgets.QPushButton("clear")
        self.btn_add = QtWidgets.QPushButton("add impurity")

        self.setupUI()



    def setupUI(self):
        self._layout.addWidget(self.btn_add,0,0,1,3)
        self._layout.addWidget(self.listWidget,1,0,1,3)
        self._layout.addWidget(self.btn_delete,2,0)
        self._layout.addWidget(self.btn_clear,2,2)


        self.btn_delete.clicked.connect(self._delete_imp)
        self.btn_clear.clicked.connect(self.listWidget.clear)

        self.setLayout(self._layout)


    def _delete_imp(self):
        imps = self.listWidget.selectedItems()
        for imp in imps:
            ix = self.listWidget.indexFromItem(imp)
            self.listWidget.takeItem(ix.row())

    def get_impurities(self):
        imp_dict = {}
        for i in range(self.listWidget.count()):
            x,y,energy = self.listWidget.item(i).get_values()
            imp_dict[(x,y)] = energy

        return imp_dict

class ImpInfoWidget(QtWidgets.QListWidgetItem):
    def __init__(self, x, y, energy):
        super().__init__()
        self.x = x
        self.y = y
        self.energy = energy

        self.setText(f"e_imp = {energy} at ({x},{y})")

    def get_values(self):
        return self.x, self.y, self.energy

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = ImpListWidget()
    widget.show()
    sys.exit(app.exec())
