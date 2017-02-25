import numpy as np

import tfsdata
from .optics import optics

def pt2delta(pt,beta0=1):
    return np.sqrt(pt**2+2*pt/beta0+1)-1

def pt2rpp(pt,beta0=1):
    """rpp=P0/P=1/(1+delta)
    """
    return 1/np.sqrt(pt**2+2*pt/beta0+1)

def pt2opd(pt,beta0=1):
    return np.sqrt(pt**2+2*pt/beta0+1)

class MadBeam(object):
    @classmethod
    def open(cls,filename,twissfile=None):
        self=cls(**tfsdata.open(filename))
        self.filename=filename
        if twissfile is not None:
            self.twiss=optics.open(twissfile)
        self.twissfile=twissfile
        return self
    def __init__(self,**args):
       self.__dict__.update(args)
    def get_full_beam(self):
       out={}
       zero=0*self.x
       one=zero+1.
       out['s']      =self.s
       out['x']      =self.x
       out['px']     =self.px
       out['y']      =self.y
       out['py']     =self.py
       out['tau']    =self.t
       out['ptau']   =self.pt
       out['tau']    =self.t
       out['ptau']   =self.pt
       out['partid'] =self.number
       out['elemid'] =0
       out['turn']   =self.turn
       out['state']  =0
       out['p0c']    =self.twiss.param['pc']*1e6
       out['e0']     =self.twiss.param['energy']*1e6
       out['m0']     =self.twiss.param['mass']*1e6
       out['gamma0'] =self.twiss.param['gamma']
       beta0         =out['p0c']/out['e0']
       out['beta0']  =beta0
       out['sigma']  =out['tau']*beta0
       out['psigma'] =out['ptau']/beta0
       opd           =pt2opd(self.pt,beta0)
       out['delta']  =opd-1
       out['rpp']    =1/opd
       out['beta']   =opd/(1/beta0+self.pt)
       out['rvv']    =beta0/out['beta']
       out['energy'] =self.e*1e6
       out['gamma']  =1/np.sqrt(1-out['beta']**2)
       out['q0']     =self.twiss.param['charge']
       out['q']      =one
       out['chi']    =one
       return out


