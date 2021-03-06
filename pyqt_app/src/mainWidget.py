from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QObject
from PyQt6.QtCore import QThread
import pyqtgraph as pg
from PyQt6.QtCore import pyqtSignal

from src.input.inputWidget import InputWidget
from src.calc.calculation import Calculation
from src.utils.progressBar import ProgressBar
from functools import partial


class MainWidget(QtWidgets.QWidget):

    def __init__(self, Nw=2):
        super().__init__()
        self.worker = {}
        self.thread = {}
        self._layout = QtWidgets.QGridLayout()

        self.Nw = 2
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.w = {}
        self.input_widget = {}
        self.spots = {}
        self.imp_dict = {}
        self.calculation = {}
        for i in range(self.Nw):
            self.w[i] = self.plot_widget.addPlot()
            self.input_widget[i] = InputWidget()
            self.spots[i] = []


        self.setupUi()

    def setupUi(self):
        self.resize(1200, 1000)
        self._layout.addWidget(self.plot_widget, 0,0,1,2)
        for i in range(self.Nw):
            self._layout.addWidget(self.input_widget[i],1,i,1,1)
            self.input_widget[i].btn_calc.clicked.connect(partial(self.calc, i))
            self.input_widget[i].btn_clear.clicked.connect(partial(self.clear, i))
            self.input_widget[i].btn_kill.clicked.connect(partial(self.kill, i))
        self._layout.setRowStretch(0, 2)
        self._layout.setRowStretch(1, 1)


        #self._layout.setRowStretch()

        self._link_views()
        self._set_plot_options()
        #self._layout.setRowStretch(0,2)
        self.setLayout(self._layout)
        self.setWindowTitle('Twisted Boundary Conditions')



    def kill(self, i):
        if self.worker is not None:
            self.worker[i].stop()



    def calc(self, i):
        self.input_widget[i].setInputEnabled(False)
        m, model_params = self.input_widget[i].get_model_params()
        p, plot_params = self.input_widget[i].get_plot_params()
        im, imp_params = self.input_widget[i].get_imp_params()
        imp_dict = self.input_widget[i].get_impurity_dict()


        # Step 2: Create a QThread object
        thread = QThread()
        self.thread[i] = thread
        # Step 3: Create a worker object
        worker = Calculation(m, model_params, p, plot_params, im, imp_params, imp_dict)
        self.worker[i] = worker
        # Step 4: Move worker to the thread
        worker.moveToThread(thread)

        # Step 5: Connect signals and slots
        thread.started.connect(worker.run_phis)
        worker.started.connect(self.input_widget[i].set_kill_btn)
        worker.finished.connect(self.input_widget[i].set_calc_btn)
        worker.killed.connect(self.input_widget[i].set_calc_btn)


        worker.killed.connect(thread.quit)
        worker.finished.connect(thread.quit)
        worker.finished.connect(partial(self.add_new_spots, i))
        thread.finished.connect(thread.deleteLater)
        worker.progress.connect(self.input_widget[i].progress_bar.update_percentage)
        worker.time_remain.connect(self.input_widget[i].progress_bar.update_time)

        worker.killed.connect(self.input_widget[i].progress_bar.reset)
        worker.killed.connect(partial(self.input_widget[i].setInputEnabled,True))
        worker.finished.connect(partial(self.input_widget[i].setInputEnabled,True))

        # Step 6: Start the thread
        thread.start()




    def add_new_spots(self, i):
        new_spots = self.worker[i].give_list_eigenvalues()

        all_spots_empty = self._all_spots_empty()
        self.spots[i].extend(new_spots)
        self.add_spots_to_plot(i, new_spots)

        if all_spots_empty:
            self.w[i].getViewBox().autoRange()


    def _all_spots_empty(self):
        all_empty = True
        for s in self.spots.values():
            if s:
                all_empty = False
            else:
                pass
        return all_empty

    def _link_views(self):
        for i in range(self.Nw):
            self.w[i].getViewBox().setXLink(view=self.w[(i+1)%self.Nw])
            self.w[i].getViewBox().setYLink(view=self.w[(i+1)%self.Nw])

    def _set_plot_options(self):
        for i in range(self.Nw):
            self.w[i].getViewBox().setMouseEnabled(x=False,y=True)
            self.w[i].getViewBox().setMouseMode(pg.ViewBox.RectMode)
            self.w[i].setLabel("bottom",text="s")
            self.w[i].setLabel("left",text="E")

    def add_spots_to_plot(self, i, new_spots):
        s = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        s.setSize(2)
        s.addPoints(new_spots)
        self.w[i].addItem(s)

    def refresh_plot(self, i):
        s = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
        s.setSize(2)
        s.addPoints(self.spots[i])
        self.w[i].clear()
        self.w[i].addItem(s)



    def clear(self, i):
            self.w[i].clear()
            self.spots[i] = []


