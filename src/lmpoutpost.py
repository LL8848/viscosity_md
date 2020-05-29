import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

from statsmodels.graphics import tsaplots


def loadlmpout(filename):

    """
        load data from a LAMMPS output file to a DataFrame
    """

    # read 2nd line of the LAMMPS file as header
    with open(filename) as file:
        header = file.readline()
        header = file.readline()
    # parse header to names of each columns
    names = header.rstrip().strip('#').split()

    # delete the "v_" prefix for some variable names
    newnames = []
    for s in names:
        if s.startswith('v_'):
            newnames.append(s[2:])
        else:
            newnames.append(s)

    df = pd.read_csv(filename,
                     delimiter = ' ',
                     skiprows = 2,
                     names = newnames
                      )


    return df


def plot1(data,dt=0.5,title=None,window=100,sharex=True):
    """
    plot a single varial against time
    dt: timestep, in fs. default 0.5 fs
    """
    step = data.iloc[:,0]
    time = dt * step * 1e-6  # dummy time, in ns, where
    y = data.iloc[:,1]
    ylabel = data.columns[1]
    running_ave = y.rolling(window=window) # running average of eta

    fig, ax = plt.subplots(2,1,sharex=sharex, constrained_layout=True)
    if title:
        fig.suptitle(title)
    else:
        fig.suptitle('Single Data plot')

    ax[0].scatter(time,y,marker="+")
    ax[0].plot(time,running_ave.mean(),c="r",label='moving average')
    ax[0].set_ylabel(ylabel)
    ax[0].legend()

    ax[1].plot(time,running_ave.std(),c='orange')
    ax[1].set_ylabel('moving window std')
    ax[1].set_xlabel('time [ns]')
#    plt.show()

    return fig, ax



def plot(data,dt=0.5,title=None,window=100):
    """
    General plot, capable of multiple variables
    """

    step = data.iloc[:,0]
    time = dt * step * 1e-6  # dummy time, in ns, where
    variables = data.columns[1:] # all variable names
    nvar = len(variables)  # number of variables

    # configure subplots. Use 2 columns and multiple rows unless only 1 var
    if nvar == 1:
        plot1(data,dt,title,window=window)
        return
    else:
        ncols = 2
        nrows = math.ceil(nvar / ncols)
    fig, ax = plt.subplots(nrows=nrows,
                           ncols=ncols,
                           sharex=True,
                           figsize=(8,nrows*6/ncols),
                           constrained_layout=True
                          )

    if title:
        fig.suptitle(title,fontsize=16)
    else:
        fig.suptitle('Multiple Data Plots',fontsize=16)


    for axi,v in zip(ax.flat,variables):
        running_ave = data[v].rolling(window=window) # running average
        axi.set_title('{}'.format(v))
        axi.scatter(time,data[v],marker="+")
        axi.plot(time,running_ave.mean(),c="r",label='moving average')
        axi.set_xlabel('time [ns]')
        axi.set_ylabel(v)
        axi.legend()

    return fig



def blockACF(df,Nblock=4,lags=50,t0=0.5,outputfreq=100000):


    # df is a pandas DataFrame loaded by loadLmpOut
    # plot ACF for Nblock consective blocks
    # t0 is MD time step in fs; = 0.5 by default

    timestep = df.iloc[:,0]  # timestep
    var = df.iloc[:,1]  # computed variable of interest



    N = len(df)
    blockSize = int(N/Nblock)               # total number of such blocks in datastream
#     blockList = []                  # container for parcelling block


    # configure subplots. Use 2 columns and multiple rows
    ncols = 2
    nrows = math.ceil(Nblock / ncols)
    fig, ax = plt.subplots(nrows=nrows,
                           ncols=ncols,
                           sharex=True,
                           figsize=(8,nrows*6/ncols),
                          constrained_layout=True
                          )
    fig.suptitle('Autocorrelation Analysis',fontsize=16)
    # Loop to chop datastream into blocks
    # and take average

    for axi,i in zip(ax.flat,list(range(1,Nblock+1))):

        ibeg = (i-1) * blockSize
        iend =  ibeg + blockSize
#         blockList.append(np.array(var[ibeg:iend]))
        tbeg = timestep.iloc[ibeg]*t0*1e-6 # block begin time
        tend = timestep.iloc[iend-1]*t0*1e-6 # block end time
        stitle = 'Block # {}, {:.2f} to {:.2f} ns'.format(i,tbeg,tend)
        # plot acf for each block
        tsaplots.plot_acf(var.iloc[ibeg:iend],
                          ax=axi,
                          title=stitle,
                          lags=lags)

        # scale x axis tick labels to time [ns]
        new_xtick_label = ["{:.2f}".format(i) \
                    for i in axi.get_xticks()*t0*outputfreq*1e-6]
        axi.set_xticklabels(new_xtick_label)

        axi.set_xlabel('Lag [ns]')
        axi.set_ylabel('ACF')
    return


def blockAverage(data,b,style='blocknum',ifprint=True):
    # data is 1d numpy array (could be a pandas series)
    data = np.array(data)
    N = len(data)     # total number of observations in data
    if style == 'blocksize':
        blockSize = b
        Nblock = int(N/blockSize) # total number of such blocks in data
    elif style == 'blocknum':
        Nblock = b
        blockSize = int(N/Nblock)

    blockAverages   = np.zeros(Nblock)    # container for parcelling block

# Loop to chop data into blocks
# and take average
    for i in range(1,Nblock+1):

        ibeg = (i-1) * blockSize
        iend =  ibeg + blockSize
        blockAverages[i-1] = np.mean(data[ibeg:iend])

    blockMean = np.mean(blockAverages)
    blockSE  = np.std(blockAverages,ddof=1)/np.sqrt(Nblock)  # block standard error
    blockEE  = blockSE * 2  # extended error (95 % confidence interval)
    if ifprint:
        print("Block size: {}".format(blockSize))
        print("Block number: {}".format(Nblock))
        print("Mean: {:.2f}".format(blockMean))
        print("Expanded uncertainty (95% confidence interval): {:.2f}".format(blockEE))
        print("Relative uncertainty {:.1f} %".format(blockEE/blockMean*100))
    return blockMean,blockEE


def blockSizing(data, isplot=True, maxBlockSize=0):

    # data should be a list or 1d numpy array or pandas series

    """This program computes the block average of a potentially correlated timeseries "x", and
    provides error bounds for the estimated mean <x>.
    As input provide a vector or timeseries "x", and the largest block size.

    Check out writeup in the following blog posts for more:
    http://sachinashanbhag.blogspot.com/2013/08/block-averaging-estimating-uncertainty_14.html
    http://sachinashanbhag.blogspot.com/2013/08/block-averaging-estimating-uncertainty.html

    Modified by Lingnan Lin on 4/20/2020
    """

    data = np.array(data)

    Ndata         = len(data)           # total number of observations in data
    print("data length: {}".format(Ndata))
    minBlockSize = 1;                        # min: 1 observation/block

    if maxBlockSize == 0:
        maxBlockSize = int(Ndata/5)        # max: 5 blocs (otherwise can't calc variance)

    NumBlocks = maxBlockSize - minBlockSize + 1   # total number of block sizes

    blockMean = np.zeros(NumBlocks)               # mean (expect to be "nearly" constant)
    blockSE  = np.zeros(NumBlocks)               # standar deviation associated with each blockSize
    blockNum  = np.zeros(NumBlocks)               # number of blocks
    blockCtr  = 0

    #
    #  blockSize is # observations/block
    #  run them through all the possibilities
    #

    for blockSize in range(minBlockSize, maxBlockSize+1):

        Nblock    = int(Ndata/blockSize)               # total number of such blocks in data
        blockAverages   = np.zeros(Nblock)                  # container for parcelling block

    # Loop to chop data into blocks
    # and take average
        for i in range(1,Nblock+1):

            ibeg = (i-1) * blockSize
            iend =  ibeg + blockSize
            blockAverages[i-1] = np.mean(data[ibeg:iend])

        blockMean[blockCtr] = np.mean(blockAverages)
        blockSE[blockCtr]  = np.std(blockAverages,ddof=1)/np.sqrt(Nblock)
        blockNum[blockCtr]  = Nblock
        blockCtr += 1

    v = np.arange(minBlockSize,maxBlockSize + 1) # Block size

    if isplot:
        fig, ax = plt.subplots(2,1,figsize=(6,8),sharex=True,constrained_layout=False)
        index = np.where(Ndata % v == 0)

        plt.subplot(2,1,1)
        plt.plot(v[index],blockSE[index],marker='o',c ='k')
        plt.title('Sizes such that Ndata % size == 0')
#         plt.xlabel('block size')
        plt.ylabel('block standard error (BSE)')
        plt.autoscale(enable=True, axis='y')
        i = 0
        for ps,py in zip(v[index],blockSE[index]):
            label = "M={:.0f}".format(blockNum[index][i])
            plt.annotate(label,
                         (ps,py),
                         textcoords="offset points", # how to position the text
                         xytext=(2,-10), # distance from text to points (x,y)
                         ha='left') # horizontal alignment can be left, right or center
            i += 1

        plt.subplot(2,1,2)
        plt.title('All sizes (strange changes may occur for Ndata % size != 0)')
        plt.plot(v, blockSE,'ro-',lw=2)
        plt.xlabel('block size')
        plt.ylabel('block standard error (BSE)')


        fig.suptitle('Block Size Analysis',fontsize=16)
#         plt.tight_layout()
        plt.show()

    return


def rave(mylist):

    # calculate running average (from beginning, not fixed-length moving window)
    sum = 0
    rave = []
    for i, x in enumerate(mylist,1):

        sum += x
        rave.append(sum / i)

    return rave


def main():
    pass


if __name__ == "__main__":
    main()
