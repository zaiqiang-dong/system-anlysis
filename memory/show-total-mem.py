import os
import sys
import csv
import pandas as pd
import getopt
import matplotlib.pyplot as plt


def show_total_data(ifile, timeRefrush):
    plt.style.use("fivethirtyeight")
    df=pd.read_csv(ifile)
    rowCnt = df.shape[0]
    lname=df.columns.values[2:].tolist()
    i = 1
    plt.ion()
    while i < rowCnt:
        ldata = df.loc[i][2:].tolist()
        plt.title("Memory Info At:" + df.iloc[i,0])
        plt.pie(ldata,labels=lname,colors=['b','m','y','c'])
        plt.pause(timeRefrush)
        i = i + 1





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
