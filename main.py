import _thread
import time
import subprocess
import getopt
import os
import sys
from memory import dumpsysMemInfo
from monkey import monkeyTest
from logcat import logcatCollect
from configDev import configDev
from report import reportByPDF

#import process moudle
from memory import showProcess
from memory import showTotalMem
from memory import showTotalPss

from logcat import processLogInfo


def printAllHelp():
    print("    -h --hlep : show this info.")
    print("    -t --times : times for monkey test. default is 10")
    print("    -c --count-action : action count for every monkey test")
    print("                        default count is 100")
    print("    -o --outdir : out put dir ,default is ./out")


opts, args = getopt.getopt(sys.argv[1:], '-h:-t:-a:-o:-v',
                           ['help', 'times', 'actions', 'outdir', 'version'])

times = 10
actionCount = 100
outdir = './out'

for opt_name, opt_value in opts:
    if opt_name in ('-h', '--hlep'):
        printHelp()
        exit()
    if opt_name in ('-t', '--times'):
        times = int(opt_value)
    if opt_name in ('-c', '--actions'):
        actionCount = int(opt_value)
    if opt_name in ('-o', '--outfile'):
        outdir = opt_value

if __name__ == "__main__":
    if not os.path.exists(outdir):
        print(outdir + " is not exit and creat it.")
        os.makedirs(outdir)
    timeValue = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    #subprocess.call("rm -rf " + outdir + "/*", shell=True)
    outdirIntermediate = outdir + "/intermediate-" + timeValue
    outdirReport = outdir + "/report-" + timeValue
    subprocess.call("mkdir " + outdirIntermediate, shell=True)
    subprocess.call("mkdir " + outdirReport, shell=True)
    print("\n"*2)
    print("*" * 100)
    print("Config Device")
    devVersion = configDev.config()
    print("Device version : " + devVersion)
    print("*" * 100)
    print("\n"*2)
    if devVersion != '':
        print("*" * 100)
        print("Do monkey test...")
        dumpsysMemInfo.initAndStart(outdirIntermediate)
        fd, p = logcatCollect.startLogcatCollect(outdirIntermediate)
        monkeyTest.doMonkeyTest(times, actionCount, outdirIntermediate)
        dumpsysMemInfo.stop()
        logcatCollect.stopLogcatCollect(fd, p)
        print("*" * 100)

        print("\n"*2)
        print("*" * 100)
        print("Process memory info")
        showProcess.report_all_procee_data(outdirIntermediate+"/dumpmem-process.csv", outdirReport)
        showTotalPss.report_total_data(outdirIntermediate+"/dumpmem-pss.csv", outdirReport)
        showTotalMem.report_total_data(outdirIntermediate+"/dumpmem-total.csv", outdirReport)
        print("*" * 100)

        print("\n"*2)
        print("*" * 100)
        print("Process logcat info")
        processLogInfo.doprocess(outdirIntermediate+"/logcat-log.txt", outdirReport)
        print("*" * 100)

        print("\n"*2)
        print("*" * 100)
        print("Create Report.pdf" + outdirReport)
        reportByPDF.createReport(outdirReport, devVersion, timeValue)
        print("*" * 100)
        print("\n"*2)
    else:
        print("*" * 100)
        print("Config dev error and end test.")
        print("*" * 100)

