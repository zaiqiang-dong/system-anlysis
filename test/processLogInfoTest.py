import sys
sys.path.append('../')

from logcat import processLogInfo

processLogInfo.doprocess(sys.argv[1] , sys.argv[2])
