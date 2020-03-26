#!/usr/bin/python3
import sys
import getopt
import _thread
import time
sys.path.append("../")
from memory import dumpsysMemInfo


def printHelp():
    print("python3 " + str(sys.argv[0]) + " -o path")
    print("    -o --outpath : out path for memory info data")


outpath = ''
opts, args = getopt.getopt(sys.argv[1:], '-h-o:-v',
                           ['help', 'outpath=', 'version'])
for opt_name, opt_value in opts:
    if opt_name in ('-h', '--hlep'):
        printHelp()
        exit()
    if opt_name in ('-o', '--outpath'):
        outpath = opt_value

if __name__ == "__main__":
    if outpath != '':
        print("Collect to " + outpath)
        try:
            _thread.start_new_thread(dumpsysMemInfo.initAndStart, (outpath,))
        except:
            print("dumpsysMemInfo thread error")
        time.sleep(5)
        dumpsysMemInfo.stop()
    else:
        print("Please attach correct args.")
        printHelp()
        exit()
