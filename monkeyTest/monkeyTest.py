import os
import sys
import time
import subprocess
import getopt
import signal
import re


def doMonkeyTest(times, actionCount, outdir):
    outfile = outdir + "/monkey-log.txt"
    if os.path.isfile(outfile):
        os.remove(outfile)
        print(outfile + " is exit, rm it.")
    else:
        print(outfile + " is not exit, rm it.")
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
        outfileFd.write("-" * 100)
        outfileFd.write("\n")
        outfileFd.write("Do " + str(count) + "TH at:" +
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        res = subprocess.Popen(
            'adb shell monkey -v-v-v ' + str(actionCount),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True)
        for l in res.stdout.readlines():
            outfileFd.write(l.decode('utf-8'))
        res.wait()
        count = count + 1
        res.terminate()
        outfileFd.write("-" * 100)
        outfileFd.write("\n" * 2)

    outfileFd.write("*" * 100)
    outfileFd.write("\n")
    tamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    outfileFd.write("End Test at " + tamp)
    outfileFd.write("\n")
    outfileFd.write("*" * 100)
    outfileFd.write("\n")


def printHelp():
    print("python3 " + str(sys.argv[0]) + " -t x")
    print("    -h --hlep : show this info.")
    print("    -t --times : times for monkey test.")
    print("    -c --count-action : action count for every monkey test")
    print("                        default count is 100")


times = 0
countAction = 100
outfile = '.'
opts, args = getopt.getopt(
    sys.argv[1:], '-h:-t:-c:-o:-v',
    ['help', 'times', 'count-action', 'outdir', 'version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h', '--hlep'):
        printHelp()
        exit()
    if opt_name in ('-t', '--times'):
        times = int(opt_value)
    if opt_name in ('-c', '--count-action'):
        countAction = int(opt_value)
    if opt_name in ('-o', '--outfile'):
        outfile = opt_value

if __name__ == "__main__":
    if times > 0:
        doMonkeyTest(times, countAction, outfile)
        exit()
    else:
        printHelp()
        exit()
