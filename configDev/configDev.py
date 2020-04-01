import os
import sys
import time
import subprocess

def configToRoot():
    croot = subprocess.call(
        'adb root',
        shell=True,
        close_fds=True)
    time.sleep(2)
    if croot != 0:
        return False
    else:
        return True
def configMemdump():
    r = subprocess.call(
        'adb shell "echo 1 > /sys/module/msm_poweroff/parameters/download_mode"',
        shell=True,
        close_fds=True)
    if r != 0:
        return False
    ret = subprocess.check_output(
        'adb shell "cat /sys/module/msm_poweroff/parameters/download_mode"',
        shell=True)

    if int(ret.decode("utf-8").strip()) != 1:
        return False
    return True

def getVersion():
    ret = subprocess.check_output(
        'adb shell "getprop ro.build.fingerprint"',
        shell=True,
        close_fds=True)
    sbuildinfo = ret.decode("utf-8").strip()
    l = sbuildinfo.split('/')
    if len(l) <= 1:
        return ''
    return l[-2]


def config():
    ret=''
    if configToRoot() and configMemdump():
        ret = getVersion()
    return ret
