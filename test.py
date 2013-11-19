import scan
import os
#import scan2d

kwds = {'lambda_um':1.064,
       'llambda':1.,
       't':0.2,
       'n_r':2.15,
       'eta':0.5,
       'n_orders':3,
       'pol':'TE'}

os.chdir("C:/Users/Caer/Documents/GitHub/easy_scan-master/data")

kwds['eta'] = 0.5
s = scan.ScanBeam('lambda_um', 0.5, 2., 200,'llambda', 0.5, 2., 200,**kwds)
s.calc()
s.save()


#kwds['eta'] = 0.8
#s = scan.ScanBeam('t', 0.1,0.9, 100,'lambda_um', 0.1,1.1,100,**kwds)
#s.calc()
#s.save()
#kwds['llambda'] = 0.8
#s = scan.ScanBeam('eta', 0.1,0.9, 100,'lambda_um', 0.1,1.1,100,**kwds)
#s.calc()
#s.save()
#kwds['llambda'] = 0.7
#s = scan.ScanBeam('eta', 0.1,0.9, 100,'lambda_um', 0.1,1.1,100,**kwds)
#s.calc()
#s.save()

import interactive_gratting