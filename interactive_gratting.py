import os.path as osp, numpy as np
import os

from guiqwt.plot import ImageDialog
from guiqwt.builder import make
from PyQt4 import QtCore, QtGui
from collections import OrderedDict
import json
import numpy

#res = grattings.r_of_lambda_and_t(save_file='sin.csv',**grattings.par_sin)

class MyImageDialog(ImageDialog):
    display_requested = QtCore.pyqtSignal()
    
    def __init__(self, directory='.'):
        self.directory = directory
        super(MyImageDialog, self).__init__(edit=False, toolbar=True, wintitle="Cross sections test",
                      options=dict(show_xsection=True, show_ysection=True))
        self.resize(600, 600)
        self.combos = OrderedDict()
        self.lay = QtGui.QFormLayout()
        
        self.refresh_button = QtGui.QPushButton('refresh')
        
        self.refresh_button.clicked.connect(self.load_dir)
        self.layout().addWidget(self.refresh_button)
        

        self.layout().addLayout(self.lay)
        
        self.image = None
        self.data = {}
        self.load_dir()
        
        
        self.display_requested.connect(self.display_data)
        self.display_requested.emit()
        
        
        

        
    def display_data(self):
        kwds = OrderedDict()
        for name, combo in self.combos.iteritems():
            try:
                kwds[name] = float(combo.currentText())
            except ValueError:
                kwds[name] = str(combo.currentText())
        key = self._str_data(kwds)
        dat, kwds = self.data[key]
        dat = 1.0-dat
        
        if not self.image:
            self.image = make.image(dat, title="Modified")
            self.get_plot().add_item(self.image)
            self.get_plot().set_axis_title(0, kwds['yname'])
            self.get_plot().set_axis_title(1, '1-R')
            self.get_plot().set_axis_title(2, kwds['xname'])
          #  self.plot_thicknesses()
            self.get_plot().legend()
        else:
            self.image.set_data(dat)
        self.image.set_xdata(kwds['xmin'], kwds['xmax'])
        self.image.set_ydata(kwds['ymin'], kwds['ymax'])
        self.get_plot().replot()
        self.get_plot().do_autoscale()

    #def plot_thicknesses(self):
     #   llambda_min = 0.
     #   llambda_max = 2.
     #   
     #   for t, col in [(0.030, 'red'),(0.050,'green'),(0.100, 'black'),(0.200, 'blue')]:
     #       c = make.curve([llambda_min, llambda_max],[t, t], color=col, title='thickness=' + str(t))
     #       self.get_plot().add_item(c)
           
    def _str_data(self, kwds):
        string = ""
        for k,v in kwds.iteritems():
            try:
                v = float(v)
            except ValueError:
                v = str(v)
            string+=k + '_' + str(v)
        return str(string)
    
    def add_data(self, data, kwds):
        
        kwds_ = kwds.copy()
        kwds_.pop('xname')
        kwds_.pop('xmin')
        kwds_.pop('xmax')
        kwds_.pop('yname')
        kwds_.pop('ymin')
        kwds_.pop('ymax')
        
        for k,v in kwds_.iteritems():
            if k in self.combos:
                if self.combos[k].findText(str(v))==-1:       
                    self.combos[k].blockSignals(True)
                    self.combos[k].addItem(str(v))   
                    self.combos[k].blockSignals(False)  
            else:
                self.combos[k] = QtGui.QComboBox()
                self.lay.addRow(QtGui.QLabel(k), self.combos[k])
                self.combos[k].currentIndexChanged.connect(self.display_data)
                self.combos[k].blockSignals(True)
                self.combos[k].addItem(str(v))
                self.combos[k].blockSignals(False)
        
        self.data[self._str_data(kwds_)] = (data, kwds)
            
    def get_data(self, n, eta, pol):
        return self.data[self._str_data(n, eta, pol)]
    
    def load_dir(self, directory=None):
        if not directory:
            directory = self.directory
        self.kwds = None
        for fname in os.listdir(directory):
            if fname.endswith('.csv'):
                with open(fname) as f:
                    kwds = json.loads(f.readline())
                    kwds = OrderedDict(sorted(kwds.iteritems(), key=lambda x: x[0])) 
                    if not self.kwds:
                        self.kwds = kwds
                    elif kwds.keys()!=self.kwds.keys() or kwds['xname']!=self.kwds['xname'] or kwds['yname']!=self.kwds['yname']:
                        print 'curve ' + fname + 'doesn t have the same scan signature as the rest of the folder, I will drop it'
                        continue
                    f.readline()
                    dat = numpy.loadtxt(f)
                    self.add_data(dat, kwds)
        
        

import os.path as osp
import guidata
_app = guidata.qapplication()
win = MyImageDialog()
win.show()
