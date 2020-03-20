import os
import sys
import csv
from datetime import datetime
import pandas as pd
import getopt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def show_total_data(ifile, timeRefrush):
    plt.style.use("seaborn-poster")
    df = pd.read_csv(ifile)
    lx = df['TimeTamp'].tolist()
    lx = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in lx]
    colName = df.columns.values.tolist()[1:]
    ylist=[]
    for i in colName:
        ylist.append(df[i].tolist())

    rowCnt = df.shape[0]

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gcf().autofmt_xdate()
    plt.legend(labels=colName,fontsize ='large')
    # plt.stackplot(lx, ylist, labels = colName)
    # plt.show()
    # plt.ion()
    i = 0
    sub=10
    while i < rowCnt:
        plt.clf()
        ylistSub=[]
        for j in ylist:
            ylistSub.append(j[i:i+sub])
        plt.stackplot(lx[i:i+sub], ylistSub, labels = colName)
        plt.pause(timeRefrush)
        i = i + sub





def printHelp():
        print("python3 " + str(sys.argv[0]) + " -i total-mem-xxx.csv")
        print("    -i --ifile : input a total mem csv file.")
        print("    -t --timeRefrush : interval of data refrush.")

ifile=''
reFrushTiem = 1.0
opts,args = getopt.getopt(sys.argv[1:],'-h-i:-t:-v',['help','ifile','timerefrash','version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h','--hlep'):
        printHelp()
        exit()
    if opt_name in ('-i', '--ifile'):
        ifile = opt_value
    if opt_name in ('-t', '--timerefrash'):
        reFrushTiem = float(opt_value)


if ifile != '':
    show_total_data(ifile,reFrushTiem)
else:
    printHelp()
    exit()
