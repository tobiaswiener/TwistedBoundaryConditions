import sys
import time

import PyQt6.QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication

class Thread(QThread):
    _signal = pyqtSignal(int)
    def __init__(self):
        super(Thread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self._signal.emit(i)

class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QProgressBar')
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.time = PyQt6.QtWidgets.QLabel("remaining time:")

        self.resize(300, 100)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pbar)
        self.vbox.addWidget(self.time)
        self.setLayout(self.vbox)
        self.show()

    def update_percentage(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)

    def update_time(self, time_remain):
        seconds = time_remain % 60
        minutes = time_remain // 50
        text = f"remaining time: {minutes} min {seconds} sec"
        self.time.setText(text)
    def reset(self):
        self.pbar.setValue(0)
        self.time.setText("remaining time:")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ProgressBar()
    ex.show()
    sys.exit(app.exec())