import os
import sys
import csv
import pandas as pd
import getopt
import matplotlib.pyplot as plt
import math
import subprocess


def show_total_data(ifile, timeRefrush):
    plt.style.use("fivethirtyeight")
    df = pd.read_csv(ifile)
    rowCnt = df.shape[0]
    lname = df.columns.values[2:].tolist()
    i = 1
    plt.ion()
    while i < rowCnt:
        plt.cla()
        ldata = df.loc[i][2:].tolist()
        plt.title("Memory Info At:" + df.iloc[i, 0])
        plt.pie(ldata, labels=lname, colors=['b', 'm', 'y', 'c'])
        plt.pause(timeRefrush)
        i = i + 1



def report_total_data(ifile, outdir=''):
    plt.style.use("fivethirtyeight")
    df = pd.read_csv(ifile)
    rowCnt = df.shape[0]
    stepRow = math.floor(rowCnt / 6)
    if outdir != '':
        outdir = outdir + "/total-meminfo"
        if os.path.exists(outdir):
            subprocess.call("rm -rf " + outdir + "/*",shell=True)
        else:
            os.mkdir(outdir)

    lname = df.columns.values[2:].tolist()

    fig = plt.figure(figsize=(19.2,12))
    ax1 = fig.add_subplot(321)
    ldata = df.loc[0*stepRow].tolist()
    ax1.pie(ldata[2:], labels=lname)
    ax1.set_title("Mem @ "+ ldata[0])

    ax2 = fig.add_subplot(322)
    ldata2 = df.loc[1*stepRow].tolist()
    ax2.pie(ldata2[2:], labels=lname)
    ax2.set_title("Mem @ "+ldata2[0])

    ax3 = fig.add_subplot(323)
    ldata3 = df.loc[2*stepRow].tolist()
    ax3.pie(ldata3[2:], labels=lname)
    ax3.set_title("Mem @ "+ldata3[0])

    ax4 = fig.add_subplot(324)
    ldata4 = df.loc[3*stepRow].tolist()
    ax4.pie(ldata4[2:], labels=lname)
    ax4.set_title("Mem @ "+ldata4[0])

    ax5 = fig.add_subplot(325)
    ldata5 = df.loc[4*stepRow].tolist()
    ax5.pie(ldata5[2:], labels=lname)
    ax5.set_title("Mem @ "+ldata5[0])

    ax6 = fig.add_subplot(326)
    ldata6 = df.loc[5*stepRow].tolist()
    ax6.pie(ldata6[2:], labels=lname)
    ax6.set_title("Mem @ "+ldata6[0])

    if outdir != '':
        plt.savefig(outdir + "/total-meminfo.png",dpi=100)
    else:
        plt.show()

