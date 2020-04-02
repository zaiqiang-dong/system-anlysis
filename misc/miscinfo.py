import sys
import os
import subprocess
import pandas as pd

coredumpList=[]
tombstonesList=[]

def collectCoreDumpInfo():
    global coredumpList
    out = subprocess.check_output('adb shell "ls /data/coredump/ -l"', shell = True)
    coredumpList = out.decode('utf-8').strip().split('\n')


def collectTombstonesInfo():
    global tombstonesList
    out = subprocess.check_output('adb shell "ls /data/tombstones/ -l"', shell = True)
    tombstonesList = out.decode('utf-8').strip().split('\n')


def processMisc(outdir):
    outdir = outdir + "/misc-info"
    if os.path.exists(outdir):
        subprocess.call('rm -rf ' + outdir + '*',shell=True)
    else:
        os.makedirs(outdir)
    collectCoreDumpInfo()
    collectTombstonesInfo()
    outCoredumpFile = outdir+"/coredump.csv"
    outTombstonesFile = outdir+"/tombstones.csv"

    dfcore = pd.DataFrame(columns=['Core dump file'])
    for f in coredumpList:
        dfcore.loc[dfcore.shape[0]] = f
    dftombas = pd.DataFrame(columns=['Tombstones file'])
    for f in tombstonesList:
        dftombas.loc[dftombas.shape[0]] = f

    dfcore.to_csv(outCoredumpFile,index=0)
    dftombas.to_csv(outTombstonesFile,index=0)





if __name__ == "__main__":
    processMisc(sys.argv[1])
