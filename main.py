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
    outdir = outdir + "/intermediate-" + timeValue
    subprocess.call("mkdir " + outdir, shell=True)
    if configDev.config():
        print("*" * 100)
        dumpsysMemInfo.initAndStart(outdir)
        fd, p = logcatCollect.startLogcatCollect(outdir)
        monkeyTest.doMonkeyTest(times, actionCount, outdir)
        dumpsysMemInfo.stop()
        logcatCollect.stopLogcatCollect(fd, p)
        print("*" * 100)
    else:
        print("*" * 100)
        print("Config dev error.")
        print("*" * 100)
