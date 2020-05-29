# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:30:41 2020

@author: lnl5
"""
import numpy as np

def Eyring(x, eta_N, sigma_E):
    """
    eta_N: Newtonian viscosity
    sigma_E: Eyring stress
    """
    return sigma_E/x*np.log(eta_N/sigma_E*x+np.sqrt((eta_N/sigma_E*x)**2+1))

