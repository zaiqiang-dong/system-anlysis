import sys
import getopt
sys.path.append("../../")
from memory import showProcess

showProcess.report_all_procee_data(sys.argv[1],  outdir=sys.argv[2])
