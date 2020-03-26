import os
import csv
import time
import re
import pandas as pd
import subprocess
import chardet
import getopt
import sys
from datetime import datetime

exit_dump=False

def getMemoryInfo(listProcess, listPss, litsTotal):
    #tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    tampPhone = subprocess.Popen(
        'adb shell "date \'+%Y-%m-%d %H:%M:%S\'"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    tamp = tampPhone.stdout.readlines()[0].decode('utf-8').strip('\n')
    res = subprocess.Popen(
        'adb shell "dumpsys meminfo"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    lines = res.stdout.readlines()

    lenOfLines = len(lines)
    splitStr = b'\n'
    idxPssProcess = lines.index(splitStr) + 1
    idxPssOOM = lines.index(splitStr, idxPssProcess, lenOfLines) + 1
    idxTotalPss = lines.index(splitStr, idxPssOOM, lenOfLines) + 1
    idxAll = lines.index(splitStr, idxTotalPss, lenOfLines) + 1

    linesOfPssProcess = lines[idxPssProcess + 1:idxPssOOM - 1]
    for l in linesOfPssProcess:
        searchObj = re.search(r' (.*)K: (.*) *\(pid (.*)\)\n',
                              l.decode('utf-8'), re.M | re.I)
        if searchObj:
            lt = [
                searchObj.group(3).strip().split(' ')[0],
                searchObj.group(2).strip(),
                int(searchObj.group(1).strip().replace(',', ''))
            ]
            if lt[1] != "dumpsys":
                listProcess.append(lt)
    linesOfTotalPss = lines[idxTotalPss + 1:idxAll - 1]
    for l in linesOfTotalPss:
        l = l.decode('utf-8')
        ltmp = l.split("K:")
        listPss.append(int(ltmp[0].strip().replace(',', '')))

    linesOfAll = lines[idxAll:]
    linesOfAll.pop()
    for l in linesOfAll:
        l = l.decode('utf-8')
        litsTotal.append(
            int(l.split(":")[1].split("K")[0].strip().replace(',', '')))

    return tamp


def collectToCsv(processCsv, pssCsv, totalMemCsv):
    global exit_dump
    while exit_dump == False:
        listProcess = []
        listPss = []
        listTatal = []
        timeTamp = getMemoryInfo(listProcess, listPss, listTatal)

        dfProcessCsv = pd.read_csv(processCsv)
        dfProcessCsv[timeTamp] = '0'

        col = dfProcessCsv.shape[1] - 1
        setpid = set(dfProcessCsv['pid'])
        for l in listProcess:
            if int(l[0]) not in setpid:
                row = dfProcessCsv["pid"].count()
                dfProcessCsv.loc[row] = 0
                dfProcessCsv.iloc[row, 0] = l[0]
                dfProcessCsv.iloc[row, 1] = l[1]
                dfProcessCsv.iloc[row, col] = l[2]
            else:
                lpid = dfProcessCsv['pid'].tolist()
                idx = lpid.index(int(l[0]))
                dfProcessCsv.iloc[idx, col] = l[2]
        dfProcessCsv.to_csv(processCsv, index=False)

        dfPssCsv = pd.read_csv(pssCsv)
        listPss.insert(0, timeTamp)
        dfPssCsv.loc[dfProcessCsv.shape[0]] = listPss
        dfPssCsv.to_csv(pssCsv, index=False)

        dfTotalCsv = pd.read_csv(totalMemCsv)
        listTatal.insert(0, timeTamp)
        dfTotalCsv.loc[dfTotalCsv.shape[0]] = listTatal
        dfTotalCsv.to_csv(totalMemCsv, index=False)

        time.sleep(5)
    print("*****************exit_dump*******************")


def initAndStart(path):
    timeValue = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    processCsv = path + "/process-" + timeValue + ".csv"
    tableTitle = [['pid', 'name']]
    os.system("touch " + processCsv)

    with open(processCsv, "w", newline='') as f:
        writer = csv.writer(f)
        for row in tableTitle:
            writer.writerow(row)

    totalPssCsv = path + "/total-pss-" + timeValue + ".csv"
    tableTitle = [[
        'TimeTamp', '.so mmap', 'Native', '.dex mmap', 'EGL mtrack',
        'GL mtrack', 'Unknown', '.oat mmap', '.apk mmap', 'Dalvik', '.art mmap',
        'Gfx dev', 'Other mmap', 'Dalvik Other', '.ttf mmap', 'Stack',
        'Other dev', '.jar mmap', 'Ashmem', 'Cursor', 'Other mtrack'
    ]]
    os.system("touch " + totalPssCsv)

    with open(totalPssCsv, "w", newline='') as f:
        writer = csv.writer(f)
        for row in tableTitle:
            writer.writerow(row)

    totalMemCsv = path + "/total-mem-" + timeValue + ".csv"
    tableTitle = [[
        'TimeTamp', 'Total RAM', 'Free RAM', 'Used RAM', 'Lost RAM', 'ZRAM'
    ]]
    os.system("touch " + totalMemCsv)
    with open(totalMemCsv, "w", newline='') as f:
        writer = csv.writer(f)
        for row in tableTitle:
            writer.writerow(row)

    collectToCsv(processCsv, totalPssCsv, totalMemCsv)


def stop():
    global exit_dump
    exit_dump = False

