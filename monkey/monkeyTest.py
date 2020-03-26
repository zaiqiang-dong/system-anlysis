import os
import sys
import time
import subprocess
import getopt
import signal
import threading
import re


def timeOutKill():
    p = subprocess.Popen(
        'ps -A -f | grep "monkey"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    for l in p.stdout.readlines():
        stmp = l.decode('utf-8')
        ret = re.search(
            r'(\w*)(\s*)(\d*)(\s*)(\d*)(.*)adb shell monkey -v-v-v (.*)', stmp,
            re.I)
        if ret:
            kp = int(ret.group(5))
            k = int(ret.group(3))
            ret = re.search(r'/bin/sh -c adb shell monkey -v-v-v', stmp, re.I)
            if ret == None:
                print("Force stop monkey ," + " kill kp = " + str(kp) +
                      " and k = " + str(k))
                os.kill(k, signal.SIGKILL)
                os.kill(kp, signal.SIGKILL)


def doMonkeyTest(times, actionCount, outdir):
    outfile = outdir + "/monkey-log.txt"
    if os.path.isfile(outfile):
        os.remove(outfile)

    outfileFd = open(outfile, 'w+')

    outfileFd.write("*" * 100)
    outfileFd.write("\n")
    tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    outfileFd.write("Start Test at " + tamp)
    outfileFd.write("\n")
    outfileFd.write("*" * 100)
    outfileFd.write("\n" * 3)

    count = 1
    while count <= times:
        print("Do " + str(count) + "TH at:" +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        outfileFd.write("-" * 100)
        outfileFd.write("\n")
        outfileFd.write("Do " + str(count) + "TH at:" +
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        t = threading.Timer(10, timeOutKill)
        t.start()
        res = subprocess.Popen(
            'adb shell monkey -v-v-v ' + str(actionCount),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True)
        for l in res.stdout.readlines():
            outfileFd.write(l.decode('utf-8'))
        res.wait()
        t.cancel()
        count = count + 1
        res.terminate()
        outfileFd.write("-" * 100)
        outfileFd.write("\n" * 2)
        time.sleep(1)

    outfileFd.write("*" * 100)
    outfileFd.write("\n")
    tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    outfileFd.write("End Test at " + tamp)
    outfileFd.write("\n")
    outfileFd.write("*" * 100)
    outfileFd.write("\n")
