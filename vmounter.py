#!/usr/bin/env python3

'''
vmounter.py [-m|-u]
-m mounts connected devices
-u unmounts devices in /media/${USER}

'''

#  import re
import subprocess
import argparse
import glob
import pprint


def alert(msg, lx=0, urgency='normal'):
    notice = "process exited with code: {}\nmessage: {}".format(lx, msg)
    args = ['notify-send', '-t', '2000', '-u', urgency, notice]
    subprocess.Popen(args)


def get_current_mounts():
    mounts = {}
    with open('/proc/mounts') as f:
        for l in f:
            if l[0] == '/':
                l = l.split()
                mounts[l[0]] = l[1]
    return mounts


def mount_user_media(mounts):
    devices = glob.glob('/dev/sd[b-z][0-9]')
    for dev in devices:
        print('checking status of dev {}'.format(dev))
        if dev not in mounts.keys():
            print("{} appears to be attached but not mounted, attempting mount".format(dev))
            args = ['udisksctl', 'mount', '-b', dev]
            sp = subprocess.Popen(args, stdout=subprocess.PIPE)
            msg = sp.communicate()[0].decode()
            lx = sp.returncode
            alert(msg, lx)


def unmount_user_media(mounts):
    for device, mountpoint in mounts.items():
        #  print('device {} mounted at {}\n'.format(device, mountpoint))

        if mountpoint.startswith('/media'):
            print('\npreparing to unmount {}'.format(device))
            args = ['udisksctl', 'unmount', '-b', device]

            sp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            msg = sp.communicate()[0].decode()
            lx = sp.returncode
            if lx == 0:
                urgency = 'normal'
            else:
                urgency = 'critical'

            alert(msg, lx, urgency)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mount', dest="mount", action='store_true', help='mount available usb')
    parser.add_argument('-u', '--unmount', dest="unmount", action='store_true', help='unmount usb')
    args = parser.parse_args()

    mounts = get_current_mounts()

    print("printing current mounts via /proc/mounts")
    pprint.pprint(mounts)

    if args.mount:
        print("mounting user media")
        mount_user_media(mounts)

    if args.unmount:
        print("unmounting user media")
        unmount_user_media(mounts)

    print("printing current mounts via /proc/mounts")
    pprint.pprint(mounts)

'''
def dismount(dev='/dev/sdc1'):
    args = ['udisksctl', 'unmount', '-b', dev]
    if subprocess.call(args):
        print('{} unmounted'.format(dev))
    else:
        print('unable to unmount dev: {}'.format(dev))
'''
