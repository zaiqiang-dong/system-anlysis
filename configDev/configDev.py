import os
import sys
import subprocess


def config():
    print("*" * 100)
    print("Config dev ...")
    print(" ")
    print("adb root.")
    subprocess.Popen(
        'adb root',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    print("sleep 2s for adb return.")
    time.sleep(2)
    subprocess.Popen(
        'adb shell "echo 1 > /sys/module/msm_poweroff/parameters/download_mode"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)

    print("open crash config.")
    res = subprocess.Popen(
        'adb shell "cat /sys/module/msm_poweroff/parameters/download_mode"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)

    for l in res.stdout.readlines():
        if int(l.decode("utf-8").strip()) == 1:
            print(" ")
            print("config success.")
            print("*" * 100)
            print("\n")
            return True
    print("\n")
    print("config failed.")
    print("*" * 100)
    print("\n")
    return False
