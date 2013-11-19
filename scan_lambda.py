import scan
import os
import numpy
import pylab

kwds = {'lambda_um':1.064,
       'llambda':0.985,
       't':0.03,
       'n_r':2.15,
       'eta':0.321,
       'n_orders':3,
       'pol':'TE'}

os.chdir("C:/Users/Caer/Documents/GitHub/easy_scan-master/data")

s = scan.Scan1DBeam('lambda_um',0.5,2.5,200,**kwds)
s.calc()
d = s.result
x = numpy.linspace(0.1,2.55,200)
pylab.plot(x,d)
pylab.xlabel('Wavelength (nm)')
pylab.ylabel('Reflectivity')