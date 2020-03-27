#!/usr/bin/python3
import sys
import getopt
import time
sys.path.append("../../")
from memory import dumpsysMemInfo


def printHelp():
    print("python3 " + str(sys.argv[0]) + " -o path")
    print("    -o --outpath : out path for memory info data")


outpath = ''
t = 15
opts, args = getopt.getopt(sys.argv[1:], '-h-o:-t:-v',
                           ['help', 'outpath=', 'time', 'version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h', '--hlep'):
        printHelp()
        exit()
    if opt_name in ('-o', '--outpath'):
        outpath = opt_value
    if opt_name in ('-t', '--time'):
        t = int(opt_value)

if __name__ == "__main__":
    if outpath != '':
        print("Collect to " + outpath)
        # try:
        #     _thread.start_new_thread(dumpsysMemInfo.initAndStart, (outpath,))
        # except:
        #     print("dumpsysMemInfo thread error")
        dumpsysMemInfo.initAndStart(outpath)
        time.sleep(t)
        dumpsysMemInfo.stop()
    else:
        print("Please attach correct args.")
        printHelp()
        exit()
