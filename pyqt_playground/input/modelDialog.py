from PyQt6 import QtGui, QtCore, QtWidgets

class ModelDialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btn = QtWidgets.QPushButton("Choose model")

        self.le = QtWidgets.QLineEdit()

        self._layout = QtWidgets.QFormLayout()
        self._layout.addRow(self.btn, self.le)

        self.setLayout(self._layout)



    def getItem(self):
        items = ("tight binding", "2 band isolator")

        item, ok = QtWidgets.QInputDialog.getItem(self, "select model dialog",
                                        "list of models", items, 0, False)

        if ok and item:
            self.le.setText(item)

        return item
