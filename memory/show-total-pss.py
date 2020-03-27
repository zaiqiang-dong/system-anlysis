import os
import sys
import time
import csv
from datetime import datetime
import pandas as pd
import getopt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Button


def show_total_data(ifile, timeRefrush, isDyanmic, out=''):
    plt.style.use("fivethirtyeight")
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
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
        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.gcf().autofmt_xdate()
        plt.ylabel("Memery Used (KB)")
        plt.title("Memory Total Pass")
        plt.stackplot(lx, ylist, labels=colName)
        plt.legend(loc=10, bbox_to_anchor=(1.0, 0.5))
        if out != '':
            plt.savefig(out)
        plt.show()


def printHelp():
    print("python3 " + str(sys.argv[0]) + " -i total-mem-xxx.csv")
    print("    -i --ifile : input a total mem csv file.")
    print("    -t --timeRefrush : interval of data refrush.")
    print("    -s --static : default is dynamic, if -s show static data.")


ifile = ''
reFrushTiem = 1.0
isDyanmic = True
opts, args = getopt.getopt(
    sys.argv[1:], '-h-i:-t:-s-v',
    ['help', 'ifile', 'timerefrash', 'static', 'version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h', '--hlep'):
        printHelp()
        exit()
    if opt_name in ('-i', '--ifile'):
        ifile = opt_value
    if opt_name in ('-t', '--timerefrash'):
        reFrushTiem = float(opt_value)
    if opt_name in ('-s', '--static'):
        isDyanmic = False

if ifile != '':
    show_total_data(ifile, reFrushTiem, isDyanmic)
else:
    printHelp()
    exit()
