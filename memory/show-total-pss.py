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

pause = False

def onclick(event):
    if event.key == '1':
        global pause
        pause = True
        print(pause)
    if event.key == '2':
        global pause
        pause = False
        print(pause)

def show_total_data(ifile, timeRefrush):
    plt.style.use("fivethirtyeight")
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
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
    #plt.legend(labels=colName,fontsize ='large')
    # plt.stackplot(lx, ylist, labels = colName)
    # plt.show()
    plt.ion()
    plt.connect('key_press_event', onclick)
    i = 0
    sub=10

    while i < rowCnt:
        plt.clf()
        ylistSub=[]
        for j in ylist:
            ylistSub.append(j[i:i+sub])
        plt.stackplot(lx[i:i+sub], ylistSub, labels = colName)
        plt.legend(loc=9,ncol=5)
        plt.pause(timeRefrush)
        i = i + sub
        while pause == True:
            input()





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
