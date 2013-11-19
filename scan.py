"""
This file is interpreted at the same time by pyhton 22 and python 27
"""
from __future__ import generators

import pickle
try:
    import subprocess
    import numpy
except ImportError:
    pass

import math
from math import sqrt
from sys import stdout

PI = math.pi

class Scan(object):
    def __init__(self, **kwds):
        self.params = kwds
        self.scans = []   
        
    def set_scan(self, var_name, min, max, n_steps):
        self.scans.append((var_name, float(min), float(max), n_steps))
    
    def scan_params(self, par_list):
        if par_list:
            values = []
            par_name, min, max, n = par_list[0]
            step = (max - min)/(n - 1)
            for index in range(n):
                self.params[par_name] = step*index + min
                values.append(self.scan_params(par_list[1:]))
            return values
        else:
            return self.calc_current()
    
    def calc_current(self):    
        return self.func(**self.params)
    
    def calc(self):
        try:
            import rodis
        except ImportError:
            pick = subprocess.check_output(['C:/python22/python.exe', __file__, pickle.dumps(self)])
            st = pick.split("===")[-1].replace('\r\n', '\n')
            self.result = numpy.array(pickle.loads(st))
            return self.result
        self.result = self.scan_params(self.scans)
        return self.result

   
class Scan2D(Scan):
    def __init__(self, xname, xmin, xmax, nstepsx, yname, ymin, ymax, nstepsy, **kwds):
        super(Scan2D, self).__init__(**kwds)
        self.xname = xname
        self.yname = yname
        self.xmin = xmin
        self.xmax = xmax
        self.nstepsx = nstepsx
        self.ymin = ymin
        self.ymax = ymax
        self.nstepsy = nstepsy
    
        self.set_scan(yname, ymin, ymax, nstepsy)
        self.set_scan(xname, xmin, xmax, nstepsx)
    
 #   def plot(self):
  #      pylab.plot(self.result)
    
    def get_filename(self):
        filename = ""
        for key,value in self.params.items():
            filename += key + '_' + str(value)
        return filename + '.csv'
    
    def save(self):
        import json
        save_file = self.get_filename()
        f = open(save_file, 'w')
        kwds = self.params.copy()
        kwds['xname'] = self.xname
        kwds['xmin'] = self.xmin
        kwds['xmax'] = self.xmax
        kwds['yname'] = self.yname
        kwds['ymin'] = self.ymin
        kwds['ymax'] = self.ymax
        for name, m, M,N in self.scans:
            kwds.pop(name)
        json.dump(kwds, f)
        #json.dump(self.scans, f)
        f.write('\n')
        f.write('[DATA]')
        f.write('\n')
        numpy.savetxt(f, numpy.array(self.result))
        f.close()
        
class Scan1D(Scan):
    def __init__(self, xname, xmin, xmax, nstepsx, **kwds):
        super(Scan1D, self).__init__(**kwds)
        self.xname = xname
        self.xmin = xmin
        self.xmax = xmax
        self.nstepsx = nstepsx
        self.set_scan(xname, xmin, xmax, nstepsx)
   
    #def plot(self):
    #    pylab.pcolor(self.result)
    
    def get_filename(self):
        filename = ""
        for key,value in self.params.items():
            filename += key + '_' + str(value)
        return filename + '.csv'
    
    def save(self):
        import json
        save_file = self.get_filename()
        f = open(save_file, 'w')
        kwds = self.params.copy()
        kwds['xname'] = self.xname
        kwds['xmin'] = self.xmin
        kwds['xmax'] = self.xmax
        for name, m, M,N in self.scans:
            kwds.pop(name)
        json.dump(kwds, f)
        #json.dump(self.scans, f)
        f.write('\n')
        f.write('[DATA]')
        f.write('\n')
        numpy.savetxt(f, numpy.array(self.result))
        f.close()
        
class Scan1DBeam(Scan1D):
    def func(self, **kwds):
        import calc_beam
        return calc_beam.r_beam(**kwds)
    
  #  def plot(self, **kwds):
  #      import numpy
  #          xx = numpy.linspace(self.xmin, self.xmax, num=self.nstepx)
      
class ScanBeam(Scan2D):
    def func(self, **kwds):
        import calc_beam
        return calc_beam.r_beam(**kwds)


class ScanCircle(Scan2D):
    def func(self, **kwds):
        import calc_circle
        return calc_circle.r_circle(**kwds)

        
class ScanBeam(Scan2D):
    def func(self, **kwds):
        import calc_beam
        return calc_beam.r_beam(**kwds)
#class ScanBeamAdim(Scan2D):
#    def func(self, lambda_=1., t_=1., n_r=3.48,eta=0.7,n_orders=3,pol=TE):
#        import calc_beam
#        return calc_beam.r_beam(llambda=1.,lambda_um=lambda_,t=t_,n_r=n_r,eta=eta,n_orders=n_orders,pol=pol)

if __name__=='__main__':
    import sys
    
    print "-------------------------------------------------------"
    f = open("c:/users/caer/Desktop/test.txt", 'w')
    f.write(sys.argv[1])
    f.close()
    print "-------------------------------------------------------"
    s = pickle.loads(sys.argv[1])
    s.calc()
    stdout.write('===')
    stdout.write(pickle.dumps(s.result))