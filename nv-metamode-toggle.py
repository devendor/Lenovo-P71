#!/usr/bin/python
import re
import sys
import os
from subprocess import call

xorg_conf = "/etc/X11/xorg.conf"
last_mode_file = os.environ.get("HOME")+"/.nv-last-metamode"
nv_cmd = '/usr/bin/nvidia-settings -a XineramaInfoOrder="%s" -a CurrentMetaMode="%s" -a [gpu:0]/GPUPowerMizerMode=%s'

with file(xorg_conf,'r') as xconf:
    try:
        modes = [i for i in xconf.readlines() if re.search('^\s*Option\s+"metamodes"', i) is not
                 None].pop().split('"')[-2].split(";")
    except:
        raise KeyError("Could not parse metamodes from xorg.conf")


with file(xorg_conf,'r') as xconf:
    try:
        xorder = [i for i in xconf.readlines() if re.search('^\s*Option\s+"nvidiaXineramaInfoOrder"', i) is not
                  None].pop().split('"')[-2]
    except:
        raise KeyError("Could not parse nvidiaXineramInfoOrder from xorg.conf")



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

    power_mode = "0" if "DFP: NULL" in modes[indx] else "2"
    cmd = nv_cmd % (xorder,modes[indx], power_mode)
    print cmd + "\n"
    call(cmd,env=os.environ,shell=True)
    with open(last_mode_file,'w') as sf:
        sf.write(str(indx))
