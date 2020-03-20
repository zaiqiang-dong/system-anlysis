import os
import sys
import csv
from datetime import datetime
import pandas as pd
import getopt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def show_pid_data(ifile, timeRefrush, pid):
    plt.style.use("fivethirtyeight")
    df = pd.read_csv(ifile)
    lx = df.columns.values.tolist()[2:]
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    ylist=df.values.tolist()
    ylshow=[]
    for l in ylist:
        if pid == l[0]:
            ylshow = l[2:]
            break;

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gcf().autofmt_xdate()
    plt.ion()
    rowCnt = len(lx)
    i = 2
    sub = 10
    while i < rowCnt:
        plt.clf()
        plt.stackplot(lx[i:i+sub], ylshow[i:i+sub], colors=['#20ab47'])
        plt.pause(timeRefrush)
        i = i + sub

def show_total_data(ifile, timeRefrush):
    plt.style.use("fivethirtyeight")
    df = pd.read_csv(ifile)
    lx = df.columns.values.tolist()[2:]
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    ylist=df.values.tolist()
    idx = 0
    for l in ylist:
        ylist[idx]=l[2:]
        idx = idx + 1

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gcf().autofmt_xdate()
    plt.ion()
    rowCnt = len(lx)
    i = 2
    sub = 10
    while i < rowCnt:
        plt.clf()
        ylistSub=[]
        for j in ylist:
            ylistSub.append(j[i:i+sub])
        plt.stackplot(lx[i:i+sub], ylistSub)
        plt.pause(timeRefrush)
        i = i + sub




def printHelp():
        print("python3 " + str(sys.argv[0]) + " -i total-mem-xxx.csv")
        print("    -i --ifile : input a total mem csv file.")
        print("    -t --timeRefrush : interval of data refrush.")
        print("    -p --pid : process num.")

ifile=''
pid=0
reFrushTiem = 1.0
opts,args = getopt.getopt(sys.argv[1:],'-h-i:-t:-p:-v',['help','ifile','timerefrash','pid','version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h','--hlep'):
        printHelp()
        exit()
    if opt_name in ('-i', '--ifile'):
        ifile = opt_value
    if opt_name in ('-p', '--pid'):
        pid = int(opt_value)
    if opt_name in ('-t', '--timerefrash'):
        reFrushTiem = float(opt_value)


if ifile != '' and pid != 0:
    show_pid_data(ifile,reFrushTiem, pid)
elif ifile != '' and pid == 0:
    show_total_data(ifile,reFrushTiem)
else:
    printHelp()
    exit()
