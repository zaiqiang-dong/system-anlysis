import os
import sys
import time
import subprocess
import getopt
import signal
import re

logcatProcess = -1
times = 2
outdir = ''
outfileFd = -1


def startLogcatCollect(outdir):
    global outfileFd
    global logcatProcess
    outfile = outdir + "logcat-log.txt"
    if os.path.isfile(outfile):
        os.remove(outfile)
        print(outfile + " file is exit, rm it.")
    else:
        print(outfile + " file is not exit.")

    tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    outfileFd = open(outfile, 'w')
    outfileFd.write("*" * 100)
    outfileFd.write("\n")
    outfileFd.write("Start Test at " + tamp)
    outfileFd.write("\n")
    outfileFd.write("*" * 100)
    outfileFd.write("\n" * 3)
    outfileFd.write("-" * 100)
    outfileFd.write("\n")
    outfileFd.close()
    outfileFd = open(outfile, 'a')

    p = subprocess.Popen(
        "adb logcat",
        stdout=outfileFd,
        stderr=subprocess.PIPE,
        shell=True,
        close_fds=True)
    logcatProcess = p


def stopLogcatCollect():
    global outfileFd
    global logcatProcess
    logcatProcess.terminate()
    logcatProcess.wait()
    outfileFd.write("-" * 100)
    outfileFd.write("\n" * 3)
    tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    outfileFd.write("*" * 100)
    outfileFd.write("\n")
    outfileFd.write("End Test at " + tamp)
    outfileFd.write("\n")
    outfileFd.write("*" * 100)
    outfileFd.write("\n")
    outfileFd.close()
    ######################################
    k = subprocess.Popen(
        'ps -A -f | grep "adb"',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        close_fds=True)
    for l in k.stdout.readlines():
        reResult = re.search(r'(\w*)(\s*)(\d*)(\d*) (.*) adb logcat',
                             l.decode('utf-8'), re.I)
        if reResult:
            os.kill(int(reResult.group(3)), signal.SIGKILL)
    k.terminate()
    k.wait()
    ######################################


def printHelp():
    print("python3 " + str(sys.argv[0]) + " -t x")
    print("    -h --hlep : show this info.")


opts, args = getopt.getopt(sys.argv[1:], '-h:-t:-o:-v',
                           ['help', 'times', 'outdir', 'version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h', '--hlep'):
        printHelp()
        exit()
    if opt_name in ('-t', '--time'):
        times = int(opt_value)
    if opt_name in ('-o', '--outdir'):
        outdir = opt_value

if __name__ == "__main__":
    startLogcatCollect(outdir)
    time.sleep(times)
    stopLogcatCollect()
