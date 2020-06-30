# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:24:54 2020

@author: Lingnan Lin, Ph.D.

lingnan.lin@nist.gov

ALL RIGHTS RESERVED

"""
# import sys
import lmpoutpost as lmp
import viscpost as vp
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

def plot(filename):
      # filename = sys.argv[1]
      df = lmp.loadlmpout(filename)
      lmp.plot(df,title=filename)
      plt.show()


def analyze(material,temp,press):
    temp = str(temp)
    press = str(press)
    material = material.upper()
    vba = vp.batch(material, temp, press, isnew=True)
    if material == 'PEC5':
        xlim=(1e6,1e11)
        ylim=(1,100)
    elif float(press) > 500:
        xlim=(1e6,1e11)
        ylim=(1,10000)    
    else:
        xlim=(1e6,1e11)
        ylim=(1,1000)
    vba.print()
    # plot viscosity vs. time for all shear rates
    vba.plotall()
    plt.show()
    # plot viscosity vs. shear rate
    vba.plot(xlim=xlim,ylim=ylim)
    plt.show()

    return vba
    # export results to a .nemd file(essentially .csv)



def copy(rootdir=r"F:\NEMD\data\new",keyword='visc',rename=False):

    # rootdir = input("root directory:\n")
    # rootdir = "F:\NEMD\data\PEC5\295K"
    targetdir = r"F:\NEMD\data\visc"
    # targetdir = os.path.join(r"F:\NEMD\data", material + '_visc')

    print("Copying files ...")

    i = 0 # counter
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if keyword in file:
                if rename:
                    # rename file with old naming convention
                    name = changeName(file)
                else:
                    # rename to standar convertion
                    name = standardname(file) 
                print(os.path.join(subdir, name))
                # copy file to the target directory
                shutil.copy(os.path.join(subdir, file),os.path.join(targetdir,name))
                i += 1
    print('Task Completed.')
    print(f'{i:} files have been copied to {targetdir}')


def standardname(basename):
    [material, temp, press, srate]= \
        basename.strip('.txt').strip('visc_').split('_')
    srate = vp.standardsrate(srate)
    
    return 'visc_' + material + '_' + temp +'_' + press + '_' + srate + '.txt'


def changeName (oldname):

    # change old naming convention to the new one
    # Example:
    # old: 295K-srate=7e-8.txt
    # new: visc_PEC6_295K_0.1MPa_7e+07.txt

    temp = oldname[:oldname.index('K')]
    srate = float(oldname[oldname.index('=')+1:oldname.rindex('.')])
    srate = '{:.0e}'.format(srate*1e15)
    newname = 'visc_' + 'PEC5_' + temp + 'K_100MPa_' + srate + '.txt'

    return newname


def main():
    pass


if __name__ == '__main__':
    main()
