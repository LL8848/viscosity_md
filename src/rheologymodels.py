# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:30:41 2020

@author: Lingnan Lin, Ph.D.

lingnan.lin@nist.gov

ALL RIGHTS RESERVED
"""
import numpy as np

def Eyring(x, eta_N, sigma_E):
    """
    x: shear rate
    eta_N: Newtonian viscosity
    sigma_E: Eyring stress
    """
    return sigma_E/x*np.log(eta_N/sigma_E*x+np.sqrt((eta_N/sigma_E*x)**2+1))



def Carreau(x, n, eta_N, lamda):
    """
    x: shear rate
    eta_N: Newtonian viscosity
    lamda: relaxation time   
    """
    return eta_N*(1+(lamda*x)**2)**((n-1)/2)