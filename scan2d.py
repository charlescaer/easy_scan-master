"""
This module is executed by python 27 only
"""
from scan import Scan
import numpy
import pylab
import json
from collections import OrderedDict

class MyScan2D:
    """
    This is the class to analyze a loaded scan
    """
    
    def __init__(self, fname):
        with open(fname) as f:
            kwds = json.loads(f.readline())
            kwds = OrderedDict(sorted(kwds.iteritems(), key=lambda x: x[0])) 
            
            xname = kwds.pop('xname')
            xmin = kwds.pop('xmin')
            xmax = kwds.pop('xmax')            
            yname = kwds.pop('yname')
            ymin = kwds.pop('ymin')
            ymax = kwds.pop('ymax')
        
            f.readline() # reads [DATA]
            dat = numpy.loadtxt(f)
            
            dim = dat.shape
            
            self.data = dat
            self.xname = xname
            self.xmin = xmin
            self.xmax = xmax
            self.stepx = (xmax - xmin)/(dim[1] - 1)
            self.yname = yname
            self.ymin = ymin
            self.ymax = ymax
            self.stepy = (ymax - ymin)/(dim[0] - 1)
            self.nstepx = dim[1]
            self.nstepy = dim[0]
            self.params = kwds
        
    def analyze(self):
        
        #self.max_cut =...self
        
        self.ymax_index = self.data.argmax()/self.nstepx
        self.xmax_index = self.data.argmax()%self.nstepx
        self.xplotmax = self.data[self.ymax_index, :]
        self.yplotmax = self.data[:,self.xmax_index]
        self.xx = numpy.linspace(self.xmin, self.xmax, num=self.nstepx)
        self.yy = numpy.linspace(self.ymin, self.ymax, num=self.nstepy)
        self.xmax_value = self.xx[self.xmax_index]
        self.ymax_value = self.yy[self.ymax_index]
        
        pylab.figure("xcut")
        pylab.title("y = " + str(self.ymax_value))
        pylab.plot(self.xx,self.xplotmax)
        pylab.xlabel(self.xname)
        pylab.ylabel('Reflectivity')

        pylab.figure("ycut")
        pylab.title("x = " + str(self.xmax_value))
        pylab.plot(self.yy,self.yplotmax)
        pylab.xlabel(self.yname)
        pylab.ylabel('Reflectivity')
        
        pylab.figure()
        pylab.xlabel(self.xname)
        pylab.ylabel(self.yname)
        pylab.pcolor(self.xx,self.yy,self.data)
        pylab.colorbar()
        
#class ScanBeamAdim(Scan2D):
#    def func(self, lambda_=1., t_=1., n_r=3.48,eta=0.7,n_orders=3,pol=TE):
#        import calc_beam
#        return calc_beam.r_beam(llambda=1.,lambda_um=lambda_,t=t_,n_r=n_r,eta=eta,n_orders=n_orders,pol=pol)

