import re
import os
import time
import pandas as pd
import csv


def doprocess(logFile, outdir=''):
    outdir = outdir + "/process-loginfo"
    if os.path.exists(outdir):
        subprocess.call('rm -rf ' + outdir + '*',shell=True)
    else:
        os.makedirs(outdir)
    regexes = [re.compile(p) for p in ['(.*)java.lang(.*)Exception(.*)', '(.*)java.lang(.*)Error(.*)', "Crash"]]
    timeValue = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    processLogCsv = outdir + "/process-loginfo-" + timeValue + ".csv"
    tableTitle = [['id', 'bug', 'log-linenumbers','times']]
    os.system("touch " + processLogCsv)

    with open(processLogCsv, "w", newline='') as f:
        writer = csv.writer(f)
        for row in tableTitle:
            writer.writerow(row)

    dfProcessLogCsv = pd.read_csv(processLogCsv)
    logFileFd = open(logFile, 'r', errors='ignore')
    line = logFileFd.readline()
    lineNumger = 1
    exceptionSet = set()
    while line != '':
        for p in regexes:
            if p.search(line):
                bug_info = line[line.find(': ') + 1:].strip('\n').strip(',')
                if len(bug_info) > 100:
                    splitPoint = []
                    i = 100
                    lenOfBug = len(bug_info)
                    while i < lenOfBug:
                        if bug_info[i] == ' ' or bug_info[i] == '.' or bug_info[i] == ',' or bug_info[i] == '_':
                            splitPoint.append(i)
                            i += 100
                        else:
                            i += 1
                    strtmp = bug_info
                    bug_info = ''
                    ps = 0
                    # print("\n")
                    # print(strtmp)
                    # print(splitPoint)
                    # print(len(strtmp))
                    for s in splitPoint:
                        s = s - ps
                        ps += s
                        bug_info += strtmp[0:s] + "\n"
                        strtmp = strtmp[s:]
                    bug_info += strtmp
                    # print(bug_info)
                    # print("\n")
                else:
                    bug_info = '\"' + bug_info + '\"'

                cBugs = set(dfProcessLogCsv['bug'])
                if bug_info not in cBugs:
                    row = dfProcessLogCsv.shape[0]
                    dfProcessLogCsv.loc[row] = 0
                    dfProcessLogCsv.iloc[row,0] = row
                    dfProcessLogCsv.iloc[row,1] = str(bug_info)
                    dfProcessLogCsv.iloc[row,2] = str(lineNumger) + ", "
                    dfProcessLogCsv.iloc[row,3] = 1
                else:
                    lbugs = dfProcessLogCsv['bug'].tolist()
                    idx = lbugs.index(bug_info)
                    times = dfProcessLogCsv.iloc[idx,3]
                    times += 1
                    dfProcessLogCsv.iloc[idx,3] = times
                    if times <= 4:
                        nums = dfProcessLogCsv.iloc[idx,2]
                        nums = nums + str(lineNumger) + ", "
                        dfProcessLogCsv.iloc[idx,2] = nums
                    elif times == 5:
                        nums = dfProcessLogCsv.iloc[idx,2]
                        nums += "..."
                        dfProcessLogCsv.iloc[idx,2] = nums

                #print(str(lineNumger)+ '--------' + line.strip('\n')[0:200])
                logFileFd.readline()
                break
        line = logFileFd.readline()
        lineNumger += 1
    dfProcessLogCsv.to_csv(processLogCsv, index=False)
