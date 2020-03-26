import getopt
import sys
sys.path.append("../monkey")

import monkeyTest


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
        monkeyTest.doMonkeyTest(times, countAction, outfile)
        exit()
    else:
        monkeyTest.printHelp()
        exit()
