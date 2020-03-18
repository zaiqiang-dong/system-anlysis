import os
import csv
import time
import re
import pandas as pd
import subprocess
import chardet
import getopt
import sys



def getMemoryInfo(listTmp):
    tamp = time.strftime("%d-%H:%M:%S", time.localtime())
    res = subprocess.Popen('adb shell "dumpsys meminfo"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    lines = res.stdout.readlines()
    for line in lines:
        searchObj = re.search(r' (.*)K: (.*) *\(pid (.*)\)\n', line.decode('utf-8'), re.M|re.I)
        if searchObj:
            l = [searchObj.group(3).strip().split(' ')[0], searchObj.group(2).strip(), searchObj.group(1).strip()]
            if l[1] != "dumpsys":
                listTmp.append(l)
        elif re.search( r'Total PSS by OOM adjustment', line.decode('utf-8'), re.M|re.I):
            break;
    return tamp

def collectToCsv(csvFile):
    while True:
        listTmp = []
        timeTamp = getMemoryInfo(listTmp)
        df = pd.read_csv(csvFile)
        df[timeTamp] = '0'
        # if df.empty == False:
        #     col = df.loc[0].count() - 1
        # else:
        #     col = 2
        col = df.loc[0].count() - 1
        setpid = set(df['pid'])
        for l in listTmp:
            if int(l[0]) not in setpid:
                row = df["pid"].count()
                df.loc[row] = 0
                df.iloc[row,0]  = l[0]
                df.iloc[row,1] = l[1]
                df.iloc[row,col] = l[2]
            else:
                lpid = df['pid'].tolist()
                idx = lpid.index(int(l[0]))
                df.iloc[idx,col] = l[2]
        df.to_csv(csvFile, index = False)
        time.sleep(1)
        print("load data ...")

def initAndStart(path):
    timeValue = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    csvFile = path+"/"+timeValue+".csv"
    tableTitle = [['pid','name'],
                    [0,0]]
    os.system("touch " + csvFile)

    with open(csvFile, "w", newline='') as f:
        writer = csv.writer(f)
        for row in tableTitle:
            writer.writerow(row)

    collectToCsv(csvFile)




def printHelp():
        print("python3 " + str(sys.argv[0]) + " -o path")
        print("    -o --outpath : out path for memory info data")


outpath = ''
opts,args = getopt.getopt(sys.argv[1:],'-h-o:-v',['help','outpath=','version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h','--hlep'):
        printHelp()
        exit()
    if opt_name in ('-o', '--outpath'):
        outpath = opt_value

if outpath != '':
    print("Collect to " + outpath)
    initAndStart(outpath)
else:
    print("Please attach correct args.")
    printHelp()
    exit()
