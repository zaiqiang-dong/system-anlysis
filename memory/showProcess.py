import os
import sys
import csv
import subprocess
import time
from datetime import datetime
import pandas as pd
import getopt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def show_pid_data(ifile, timeRefrush, pid):
    plt.style.use("fivethirtyeight")
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    df = pd.read_csv(ifile)
    lx = df.columns.values.tolist()[2:]
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    ylist = df.values.tolist()
    ylshow = []
    for l in ylist:
        if pid == l[0]:
            ylshow = l[2:]
            break

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gcf().autofmt_xdate()
    plt.ion()
    rowCnt = len(lx)
    i = 2
    sub = 3
    while i < rowCnt:
        plt.clf()
        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.ylabel("Memery Used (KB)")
        plt.title("Memory Usd (Pid = " + str(pid) + ")")
        plt.stackplot(lx[i:i + sub], ylshow[i:i + sub], colors=['#20ab47'])
        plt.pause(timeRefrush)
        i = i + sub


def show_total_data(ifile, timeRefrush):
    plt.style.use("fivethirtyeight")
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    df = pd.read_csv(ifile)
    lx = df.columns.values.tolist()[2:]
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    ylist = df.values.tolist()
    idx = 0
    for l in ylist:
        ylist[idx] = l[2:]
        idx = idx + 1

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gcf().autofmt_xdate()
    plt.ion()
    rowCnt = len(lx)
    i = 2
    sub = 3
    while i < rowCnt:
        plt.clf()
        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.ylabel("Memery Used (KB)")
        plt.title("Memory Total All Process")
        ylistSub = []
        for j in ylist:
            ylistSub.append(j[i:i + sub])
        plt.stackplot(lx[i:i + sub], ylistSub)
        plt.pause(timeRefrush)
        i = i + sub

def report_all_procee_data(ifile, outdir=''):
    plt.style.use("fivethirtyeight")
    df = pd.read_csv(ifile)
    lx = df.columns.values.tolist()[2:]
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    ylist = df.values.tolist()

    outdir = outdir + "/process-memory-info"
    if os.path.exists(outdir):
        subprocess.call('rm -rf ' + outdir + '*',shell=True)
    else:
        os.makedirs(outdir)

    for l in ylist:
        plt.clf()
        plt.figure(figsize=(19.2,6.4))
        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.ylabel("Memery Used (KB)")
        plt.title("Memory Usd (PName = " + str(l[1]) + ")")
        plt.stackplot(lx, l[2:])
        if outdir != '':
            plt.savefig(outdir +"/"+ str(l[1]).replace('.','_') + ".png", dpi=100)
        else:
            plt.show()
        plt.close()


