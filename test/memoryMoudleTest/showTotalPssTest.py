import sys
import getopt
sys.path.append("../../")

from memory import showTotalPss

showTotalPss.report_total_data(sys.argv[1], outdir=sys.argv[2])
