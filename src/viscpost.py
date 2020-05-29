# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:31:06 2020

@author: Lingnan Lin
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import lmpoutpost as lmp
from rheologymodels import Eyring
from scipy.optimize import curve_fit
from math import ceil

class Viscdata:
    
    def __init__(self,material,temp,press,srate,data,
                dt=0.5,outputfreq=100000):
        self.material = material
        self.temp = temp # temperature [K]
        self.press = press # pressure [MPa]
        self.srate = standardsrate(srate) # shear rate [s^-1]
        self.dt = dt # timestep in fs; =0.5 by default
        self.data = data
        self.step = data.iloc[:,0]
        self.time = self.dt * self.step * 1e-6 # in ns
        self.strain = float(srate)*self.time*1e-9
        self.visc = data.iloc[:,1] # viscosity
        self.sslength = 20  # length of steady-state [ns]. Default: 20 ns
        self.ssdata = self.data.iloc[-int(self.sslength/(self.dt*1e-6)/outputfreq):]
        self.outputfreq = outputfreq # = 100000 by default

        
#    def plot(self):
#        srate = float(self.srate)
#        visc_running_ave = self.visc.rolling(window=10) # running average of eta
#
#        fig, ax = plt.subplots(2,1,sharex=True)
#        fig.suptitle(f'NEMD data of {self.material} for {self.temp}, {self.press}' + 
#                    f'\n shear rate = {srate:.0e} 1/s'
#                    )
#
#        ax[0].scatter(self.time,self.visc,marker="+")
#        ax[0].plot(self.time,visc_running_ave.mean(),c="r",label='moving average')
#        ax[0].axvline(1/srate*1e9,linestyle='--',c='b',label='1/srate={:.1f} ns'.format(1/srate*1e9))
#        ax[0].set_ylabel('viscosity [mPa s]')
#        ax[0].legend()
#
#        ax[1].plot(self.time,visc_running_ave.std(),c='orange')
#        ax[1].set_ylabel('moving window std')
#        ax[1].set_xlabel('time [ns]')
#        ax[1].axvline(1/srate*1e9,linestyle='--',c='b',label='1/srate={:.1f} ns'.format(1/srate*1e9))
#        plt.show()
    
    def info(self,ifprint=True):
        # srate = standardsrate(self.srate)
        # s = f'{self.material}, {self.temp}, {self.press}, {self.srate} 1/s'
        # material  = self.material
        s  = '{}, {}, {}, {} 1/s'.format(self.material,
                                              self.temp,
                                              self.press,
                                              self.srate)
        if ifprint:
            print(s)
        return s
    
    
    def plot(self,window=50):
        srate = float(self.srate)
        title = f'NEMD data of {self.material} for {self.temp}, {self.press}' + f'\n shear rate = {srate:.0e} 1/s'
        fig, ax = lmp.plot1(self.data,dt=self.dt,title=title,window=window,sharex=True)
        ax[0].set_ylabel('viscosity [mPa s]')
        ax[0].axvline(1/srate*1e9,linestyle='--',
                      c='b',label='t=1/srate={:.1f} ns'.format(1/srate*1e9))
        ax[0].legend()
        # draw a separate x-axis on top for the strain
        ax0top =ax[0].twiny()
        ax0top.set_xticks(ax[0].get_xticks())
        ax0top.set_xbound(ax[0].get_xbound())
        new_xtick_label = ["{:.1f}".format(i) \
                           for i in ax[0].get_xticks()*float(self.srate)*1e-9]
        ax0top.set_xticklabels(new_xtick_label)
        # another method
        # new_tick_locations = linspace(self.strain.iloc[0],self.strain.iloc[-1],6)
        # axax0top.set_xticklabels(tick_function(new_tick_locations))
        # axax0top.plot(self.strain,self.visc,marker)
        # axax0top.cla()
        ax0top.set_xlabel('strain [-]')
        plt.show()
        
        return fig,ax
    
    def ssplot(self,window=50):
        srate = float(self.srate)
        title = f'Final Steady-state data' + f'\n {self.material}, {self.temp}, {self.press}, {srate:.0e} 1/s'
        fig, ax = lmp.plot1(self.ssdata,dt=self.dt,title=title,window=window)
        ax[0].set_ylabel('viscosity [mPa s]')
        ax[0].legend()
        

    def acf(self,data=None,Nblock=4,lags=50):
        if data is None:
            data = self.data
        lmp.blockACF(data,Nblock,lags,self.dt)
        
    def setss(self,ts):
        """
            set steady state start at ts [ns]
        """
        ts_step = int(ts / (self.dt * 1e-6))
        self.sslength = self.time.iloc[-1] - ts
        self.ssdata = self.data[self.step >= ts_step]
        print("Set steady state as from {} ns to {} ns".format(ts,self.time.iloc[-1]))
        print("Production length: {} ns".format(self.sslength))
    
    
    def setss1(self,t_begin,t_end):
        
        """
        set steady-state as from t_begin to t_end
        """
        
        step_begin = int(t_begin / (self.dt * 1e-6))
        step_end = int(t_end / (self.dt * 1e-6))
        self.sslength = t_end - t_begin
        self.ssdata = self.data[(self.step >= step_begin) \
                                & (self.step <= step_end)]
        print("Set steady state as from {} ns to {} ns".format(t_begin,t_end))
        print("Production length: {} ns".format(self.sslength))        


    def average(self,blocknum=10,ifprint=False):
        if ifprint:
            print("Production length: {:.1f} ns".format(self.sslength))        
        # here, error is 95 % confidence interval
        mean,error = lmp.blockAverage(self.ssdata.visc,
                                      blocknum,
                                      style='blocknum',
                                      ifprint=ifprint)
        
        return mean,error


class ViscBatch:
    
    def __init__(self,visclist,results):
        self.material = visclist[0].material
        self.temp = visclist[0].temp
        self.press = visclist[0].press
        self.srate = [f.srate for f in visclist]
        self.visclist = visclist
        self.results = results
        # self.dict = dict()
        # for f in visclist:
        #     self.dict[f.srate] = f


    def info(self,ifprint=False):
        # srate = standardsrate(self.srate)
        # s = f'{self.material}, {self.temp}, {self.press}, {self.srate} 1/s'
        # material  = self.material
        s  = '{}, {}, {}'.format(self.material,
                                              self.temp,
                                              self.press)
        if ifprint:
            print(s)
        return s
 
       
    def get(self,srate):
        """
        retrieve the ViscData via the corresponding shear rate as the key
        """
        srate = standardsrate(srate)
        file_exist = False # flag
        for viscdata in self.visclist:
            if srate == viscdata.srate:
                file_exist = True
                return viscdata
        if not file_exist:
            print(f"File with {srate} not found")
        

    def plot(self,model=Eyring,color='b',xlim=(1e6,1e11),ylim=(1,100)):
        """
        plot viscosity versus shear rate
    
        """
        # plot the data
        plt.errorbar(self.results.iloc[:,0],self.results.iloc[:,1],
                      yerr=self.results.iloc[:,2],
                      ls='none',marker='o',color=color)
        # plot the fit
        popt,perr = self.fit(Eyring)
        x = np.logspace(np.log10(xlim)[0],np.log10(xlim)[1],100)
        y = model(x,*popt)
        plt.plot(x,y,c=color,label=self.info())
                
        # plt.title(f"{self.material} at {self.temp}, {self.press}")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlim(*xlim)
        plt.ylim(*ylim)
        plt.xlabel('Shear rate [1/s]')
        plt.ylabel('Viscosity [mPa s]')
        
        eta_N, sigma_E = popt
        ee_eta_N, ee_sigma_E = 2 * perr  
        # note: perr is standard error
        # expanded error = coverage factor * standard error
        
        
        print('-'*60)
        print("Fit parameters:")
        print(f"eta_N: {eta_N:.1f} +- {ee_eta_N:.1f}")
        print(f"sigma_E: {sigma_E:.1e} +- {ee_sigma_E:.1e}")
        print("-"*60)      
        # note: perr is standard error not confifence interval
        return [eta_N,ee_eta_N],[sigma_E,ee_sigma_E]


    def axplot(self,ax,model=Eyring,
             color='b',xlim=(1e6,1e11),ylim=(1,100)):
        """
        for use of multiple plots
        plot viscosity versus shear rate
        """
        # plot the data
        ax.errorbar(self.results.iloc[:,0],self.results.iloc[:,1],
                     yerr=self.results.iloc[:,2],
                     ls='none',marker='o',color=color)
        # plot the fit
        popt,perr = self.fit(Eyring)
        x = np.logspace(np.log10(xlim)[0],np.log10(xlim)[1],100)
        y = model(x,*popt)
        ax.plot(x,y,c=color,label=self.info())
                
        # plt.title(f"{self.material} at {self.temp}, {self.press}")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_xlabel('Shear rate [1/s]')
        ax.set_ylabel('Viscosity [mPa s]')
        
        eta_N, sigma_E = popt
        ee_eta_N, ee_sigma_E = 2 * perr  
        # note: perr is standard error
        # expanded error = coverage factor * standard error
        
        print('-'*60)
        print("Fit parameters:")
        print(f"eta_N: {eta_N:.1f} +- {ee_eta_N:.1f}")
        print(f"sigma_E: {sigma_E:.1e} +- {ee_sigma_E:.1e}")
        print("-"*60)      
        # note: perr is standard error not confifence interval
        
        return [eta_N,ee_eta_N],[sigma_E,ee_sigma_E],ax

    
    def plotall(self):
        """
        plot time-series for each srate
        """
        n = len(self.visclist)
        ncols = 2
        nrows = ceil(n / ncols)
        fig, ax = plt.subplots(nrows=nrows,ncols=ncols,sharex=False,
                               figsize=(8,nrows*4/ncols),
                               constrained_layout=True
                               )
        fig.suptitle(self.info(),fontsize=16)
        for f,axi in zip(self.visclist,ax.flat):
            axi.set_title(f.srate)
            axi.scatter(f.time,f.visc,marker="+")
            axi.axvline(1/float(f.srate)*1e9,linestyle='--',
                      c='b',label='t=1/srate={:.1f} ns'.format(1/float(f.srate)*1e9))
            
            running_ave = f.visc.rolling(window=100)
            axi.plot(f.time,running_ave.mean(),c="r",label='moving average')
    #     ax[0].scatter(time,y,marker="+")
    # ax[0].plot(time,running_ave.mean(),c="r",label='moving average')
    # ax[0].set_ylabel(ylabel)
    # ax[0].legend()    
        plt.show()



    
    def fit(self,model):
        """
        model = Eyring,Carreau, ...
        """
        print(f"Fit model: {model.__name__}")
        # print(f"Fitting info:")
        xdata = self.results['srate'].to_numpy()
        ydata = self.results['viscosity'].to_numpy()
        yerror = self.results['error'].to_numpy()
        # popt: optimized parameters
        # pcov: covariance matrix
        
            
        popt, pcov = curve_fit(model,xdata,ydata,sigma=yerror,p0=[10,1e10],
                               absolute_sigma=True,
                               bounds=(0,np.inf),
                               method='trf',
                               ftol=1e-12,xtol=1e-12,gtol=1e-12,verbose=2)
           
# ftol=1e-12,xtol=1e-12,
        # perr: standard errors of the parameters
        # equal to square root of the diagnol of the covariance matrix
        perr = np.sqrt(np.diag(pcov))     
    
        return popt,perr


    def erying(self,**kwargs):
        
        popt,perr = self.plot(model=Eyring,**kwargs)

        eta_N, sigma_E = popt
        ee_eta_N, ee_sigma_E = 2 * perr  # expanded error
        
        print('-'*60)
        print("Fit parameters:")
        print(f"eta_N: {eta_N:.1f} +- {ee_eta_N:.1f}")
        print(f"sigma_E: {sigma_E:.1e} +- {ee_sigma_E:.1e}")
        print("-"*60)
        

        return [eta_N,ee_eta_N],[sigma_E,ee_sigma_E]
        
    

    
    def export(self):
        """
        export the results to a file (.nemd)
        for the use of OriginLab plot
        """
        filename = "{}_{}_{}.nemd".format(self.material,self.temp,self.press)
        directory = r"F:\NEMD\data\processed"
        path = os.path.join(directory,filename)
        self.results.to_csv(path,
                            columns=['srate','viscosity','error'],
                            index=False)
        print(f"Saved to {path}")
    
    
    def print(self):
        print("Results:")
        pd.set_option('precision',1)
        print(self.results.to_string(index=False))


def loadvisc(filename,ifplot=True):
    """
        load data from a LAMMPS output file to a DataFrame
    """
    if os.path.isabs(filename):
        basename = os.path.basename(filename)
    else:
        basename = filename
    # parse filename:
    [material, temp, press, srate]= \
        basename.strip('.txt').strip('visc_').split('_')
       
    df = lmp.loadlmpout(filename)    
    
    vd = Viscdata(material,temp,press,srate,df)
    
    if ifplot:
        vd.plot()
        
    return vd 


def readvisc(material,temp,press,srate,ifplot=True):
    """
    read a nemd file by state point parameters
    default location: 'F:\\NEMD\\data\\visc'
    """
    temp = str(temp).upper()
    press = str(press)
    srate = standardsrate(srate)
    # root = "F:\\NEMD\\data\\" + material + '_visc'
    root = r"F:\NEMD\data\visc"
    flag = False
    for root, subdirs, files in os.walk(root):
        for file in files:
            if (material in file) and (temp in file) \
                and (press in file) and (srate in file):    
                f = loadvisc(os.path.join(root,file),ifplot=ifplot)
                flag = True
    if not flag:
        print("File not found!")
        return
    else:
        return f


def batch(material,temp,press,isnew=False):
    """
    calculate blcok average for a batch of nemd files
    return a ViscBatch instance
    """
    temp = str(temp)
    press = str(press)
    if isnew:
        root = r"F:\NEMD\data\new"
    else:
        root = r"F:\NEMD\data\visc"
        # root = "F:\\NEMD\\data\\" + material + '_visc'
    print("\n")
    print("*"*20)
    print(f"* {material},{temp}K,{press:3}MPa *")
    print("*"*20)
    print("Data location: " + root)
    print("-"*60)
    # create a container for the computed results
    results = []
    # create a list that stores the Viscdata of each srate
    visclist = [] 
    for root, subdirs, files in os.walk(root):
        for file in files:
            if (material in file) and (temp in file) and (press in file):
                abspath = os.path.join(root,file) # absolute path
                # print(abspath)
                if os.path.isfile(abspath):
                    f = loadvisc(abspath,ifplot=False)
                    srate = float(f.srate)
                    mean, error = f.average()
                    results.append([srate,mean,error,error/mean*100])
                    
                    visclist.append(f)
                else:
                    print("File doesn't exit - " + abspath)
                # print("-"*60)
    # results = np.array(results)
    results = pd.DataFrame(results,
                           columns=['srate','viscosity','error','rerror%'])
    results = results.sort_values('srate')
    
    # sort visclist by srate
    visclist.sort(key=lambda ff: float(ff.srate) )
    return ViscBatch(visclist,results)




def standardsrate(srate):
    """
    convert different formats of shear rate to a standard format:
    XXe+XX
    Example: 1e6 -> 1e+06
    Accepts both string and float 
    """
    
    return "{:.0e}".format(float(srate)) 



def main():
    pass


if __name__ == "__main__":
    main()
