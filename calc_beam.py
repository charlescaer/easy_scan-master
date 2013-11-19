from rodis import *

def r_beam(lambda_um=1.064,
           llambda=1.,
           t=0.2,
           n_r=2.0,
           eta=0.77,
           n_orders=3,
           pol='TM'):
    set_lambda(lambda_um)
    set_N(n_orders)   
    set_polarisation(pol)
    
    # make device
    GaAs = Material(n_r)
    air  = Material(1.0)
    
    front  = Slab( air(llambda) )
    period = Slab( air(llambda*(1-eta)/2) + GaAs(llambda*eta) + air(llambda*(1-eta)/2))
    back   = Slab( air(llambda)  )
    
    grating = Stack( front(1.) + period(t) + back(1.))
    
    # start calculations
    grating.calc()
    return grating.diffr_eff().R(0)