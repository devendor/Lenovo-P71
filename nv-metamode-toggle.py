#!/usr/bin/python
import re
import sys
import os
from subprocess import call

xorg_conf = "/etc/X11/xorg.conf"
last_mode_file = os.environ.get("HOME")+"/.nv-last-metamode"
nv_cmd = '/usr/bin/nvidia-settings -a CurrentMetaMode="%s"'

with file(xorg_conf,'r') as xconf:
    try:
        modes = [i for i in xconf.readlines() if re.search('^\s*Option\s+"metamodes"', i) is not
                 None].pop().split('"')[-2].split(";")
    except:
        raise KeyError("Could not parse metamodes from xorg.conf")

if os.path.exists(last_mode_file):
    last_mode = int(file(last_mode_file,'r').read(1))
else:
    last_mode = 0

if len(sys.argv) == 1:
    for i in range(0,len(modes)):
        print "%s: %s" % (i,modes[i])
else:
    try:
        indx = int(sys.argv[-1])
    except ValueError:
        indx = last_mode + 1

    if indx >= len(modes):
        indx = 0

    cmd = nv_cmd % modes[indx]
    print cmd + "\n"
    call(cmd,env=os.environ,shell=True)
    with open(last_mode_file,'w') as sf:
        sf.write(str(indx))
