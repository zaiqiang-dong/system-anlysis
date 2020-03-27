import sys
import time
import getopt
sys.path.append("../../")
from logcat import logcatCollect


def printHelp():
    print("python3 " + str(sys.argv[0]) + " -t x")
    print("    -h --hlep : show this info.")


outdir = './'
times = 2
opts, args = getopt.getopt(sys.argv[1:], '-h-t:-o:-v',
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
    fd, p = logcatCollect.startLogcatCollect(outdir)
    time.sleep(times)
    logcatCollect.stopLogcatCollect(fd, p)
