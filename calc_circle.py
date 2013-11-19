from rodis import *
import math
from math import sqrt
from sys import stdout

PI = math.pi


def r_circle(lambda_laser=1.064,
             llambda_x=1.0,
             llambda_y=1.0,
             radius=0.5,
             thickness=0.2,
             n_slabs=10,
             n_r=3.4,
             polar_rad=0.,
             n_modes_x_or_y=3):
    set_alpha(0.0)
    set_delta(0.0)
    set_psi(polar_rad)
    set_dzeta(PI/2)
    set_lambda(lambda_laser)
    set_Nx(n_modes_x_or_y)
    set_Ny(n_modes_x_or_y)
    
    center_x = llambda_x/2.
    center_y = llambda_y/2.
    thickness_slab = llambda_x/n_slabs
    
    #- make materials -#
    Air         = Material(1.0)
    GaAs        = Material(n_r)

    def get_slab(x):
        """
        Returns the slab that is centered around coordinate x
        """
    
        if abs(x - center_x) > radius:
            return Slab(GaAs(llambda_y))
        else:
            hole_length = 2*sqrt(abs(x - center_x))
            return Slab(GaAs((llambda_y - hole_length)/2) + Air(hole_length) + GaAs((llambda_y - hole_length)/2))
    slabs = [get_slab(index*thickness_slab)(thickness_slab) for index in range(n_slabs)]
    temp = None
    for slab in slabs:
        if not temp:
            temp = slab
        else:
            temp = temp + slab
    membrane = Section(temp)
    air_space = Section(Slab(Air(llambda_y))(llambda_x))
    device = Stack(air_space(1.) + membrane(thickness) + air_space(1.))

    #- make grating   -#
    device.calc()
    
    return device.diffr_eff().R(0,0)


def scan(llambda_min=0.1,
         llambda_max=2.,
         n_llambdas=5,
         t_min=0.2,
         t_max=2.0,
         n_ts=5,
         n_r=3.4,
         eta=0.1,
         n_orders=3,
         polar_rad=0.,
         n_slabs=10):
    
    reflectivity = []
    step_llambda = (llambda_max - llambda_min)/n_llambdas
    step_ts = (t_max - t_min)/n_ts
    
    for j in range(n_ts): ###!%£^* Don't have numpy in python 2.2 !!!
        reflectivity_of_t = []
        for i in range(n_llambdas):
            llambda = llambda_min + step_llambda*i
            t = t_min + step_ts*j
            radius = llambda*eta*0.5
            # rodis data
            r = r_circle(lambda_laser=1.064,
                         llambda_x=llambda,
                         llambda_y=llambda,
                         radius=radius,
                         thickness=t,
                         n_slabs=n_slabs,
                         n_r=n_r,
                         polar_rad=polar_rad,
                         n_modes_x_or_y=n_orders)
            
            reflectivity_of_t.append(r)
        reflectivity.append(reflectivity_of_t)

    for reflectivity_of_t in reflectivity:
        first = True
        for r in reflectivity_of_t:
            if not first:
                stdout.write(',')
            first = False
            stdout.write(str(r))
            
        stdout.write('\n')
    

if __name__=='__main__':
    import sys
    print """==="""
    kwds = {'llambda_min':float(sys.argv[1]),
            'llambda_max':float(sys.argv[2]),
            'n_llambdas':int(sys.argv[3]),
            't_min':float(sys.argv[4]),
            't_max':float(sys.argv[5]),
            'n_ts':int(sys.argv[6]),
            'n_r':float(sys.argv[7]),
            'eta':float(sys.argv[8]),
            'n_orders':int(sys.argv[9]),
            'polar_rad':float(sys.argv[10]),
            'n_slabs':int(sys.argv[11])}
    scan(**kwds)