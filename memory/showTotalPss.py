import os
import sys
import time
import csv
import subprocess
from datetime import datetime
import pandas as pd
import getopt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Button


def show_total_data(ifile, timeRefrush=1, isDyanmic=False, outdir=''):
    if outdir != '':
        outdir = outdir + "/total-pss-info"
        if os.path.exists(outdir):
            subprocess.call("rm -rf " + outdir + "/*",shell=True)
        else:
            os.mkdir(outdir)
    plt.style.use("fivethirtyeight")
    df = pd.read_csv(ifile)
    lx = df['TimeTamp'].tolist()
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    colName = df.columns.values.tolist()[1:]
    ylist = []
    for i in colName:
        ylist.append(df[i].tolist())

    rowCnt = df.shape[0]
    if isDyanmic:
        plt.ion()
        i = 0
        sub = 3
        while i < rowCnt:
            plt.clf()
            plt.gca().xaxis.set_major_formatter(
                mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            plt.gcf().autofmt_xdate()
            plt.ylabel("Memery Used (KB)")
            plt.title("Memory Total Pass")
            ylistSub = []
            for j in ylist:
                ylistSub.append(j[i:i + sub])
            plt.stackplot(lx[i:i + sub], ylistSub, labels=colName)
            plt.legend(loc=10, bbox_to_anchor=(1.0, 0.5))
            plt.pause(timeRefrush)
            i = i + sub
    else:
        plt.figure(figsize=(19.2,7.2))
        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.ylabel("Memery Used (KB)")
        plt.title("Memory Total Pass")
        plt.stackplot(lx, ylist, labels=colName)
        plt.legend(loc=10, bbox_to_anchor=(1.0, 0.5))

        if outdir != '':
            plt.savefig(outdir+"/totol-pss-info.png",dpi=100)
        else:
            plt.show()

    plt.close()



def report_total_data(ifile, outdir):
    if outdir != '':
        outdir = outdir + "/total-pss-info"
        if os.path.exists(outdir):
            subprocess.call("rm -rf " + outdir + "/*",shell=True)
        else:
            os.mkdir(outdir)
    plt.style.use("fivethirtyeight")
    df = pd.read_csv(ifile)
    lx = df['TimeTamp'].tolist()
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    colName = df.columns.values.tolist()[1:]
    ylist = []
    for i in colName:
        ylist.append(df[i].tolist())

    plt.figure(figsize=(19.2,7.2))
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gcf().autofmt_xdate()
    plt.ylabel("Memery Used (KB)")
    plt.title("Memory Total Pass")
    plt.stackplot(lx, ylist, labels=colName)
    plt.legend(loc=10, bbox_to_anchor=(1.0, 0.5))

    if outdir != '':
        plt.savefig(outdir+"/totol-pss-info.png",dpi=100)
    else:
        plt.show()

    plt.close()

