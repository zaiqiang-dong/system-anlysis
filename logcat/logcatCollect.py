import os
import sys
import time
import subprocess
import getopt
import signal
import re


def startLogcatCollect(outdir):
    outfile = outdir + "/logcat-log.txt"
    if os.path.isfile(outfile):
        os.remove(outfile)

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
    return outfileFd, logcatProcess


def stopLogcatCollect(outfileFd, logcatProcess):
    logcatProcess.terminate()
    logcatProcess.wait()
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
