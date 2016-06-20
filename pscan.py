#!/usr/bin/env python3

import os
import random
import subprocess
import argparse

topdir =  '/media/vic/44c6b850-c884-4945-9799-9867dddb0949'
viddirs = [ os.path.join(topdir, 'Brazzers'), 
            os.path.join(topdir, 'sports/hockey')]
found = []

def get_vids(top):
   for root, dirs, files in os.walk(top, topdown=False):
       for f in files:
           if f.endswith(('mp4', 'avi', 'wmv', 'flv')):
               found.append(os.path.join(root, f))

   random.shuffle(found)
   return found
   '''
   for vid in found[0:10]:
       play(vid)
   '''

def grep_vids(vids, pat):
    matches = []
    import re
    rx = re.compile(pat)
    for f in vids:
        if re.search(rx, f):
            print('found {}'.format(f))
            matches.append(f)

    return matches

            
def play(vid):
    args = [ 'cvlc', "-f", vid ]
    p = subprocess.call(args)
    d = input("need more [Y/n]")
    if d == "n":
        quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--search', dest="find", action='store', help='search term')
    args = parser.parse_args()

    if os.path.ismount(topdir):
        for viddir in viddirs:
            vids = get_vids(viddir)
    else:
        print('filesystem not mounted')
        quit()

    if args.find:
        print("see find as {}".format(args.find))
        vids_to_play = grep_vids(vids, args.find)
    else:
        vids_to_play = vids

    for vid in vids_to_play:
        play(vid)



