# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:53:05 2020

@author: Lingnan Lin, Ph.D.

lingnan.lin@nist.gov

ALL RIGHTS RESERVED
"""

import os
import shutil
# import sys

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



def copy(keyword,rootdir,targetdir,ifrename=False):
    

    # rename and copy
    
    i = 0 # counter
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if keyword in file:                
                if ifrename:
                    # rename file
                    name = changeName(file)
                else:
                    name = file                   
                print(os.path.join(subdir, name))
                # copy file to the target directory
                shutil.copy(os.path.join(subdir, file),os.path.join(targetdir,name))
                i += 1
    print('Task Completed.')
    print(f'{i:} files have been copied to {targetdir}')


    
def main():
    
    keyword = 'srate'
    rootdir = input("root directory:\n")
    # rootdir = "F:\NEMD\data\PEC5\295K"
    targetdir = r"F:\NEMD\data\PEC6_visc"
    print("Copying files ...")
    # rootdir = "F:\\NEMD\\data\\PEC6\\373K\\100MPa"
    # targetdir = "F:\\NEMD\\data\\PEC6_visc"
    copy(keyword,rootdir,targetdir,ifrename=False)


if __name__ == '__main__':
    main()