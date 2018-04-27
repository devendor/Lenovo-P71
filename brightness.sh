#!/bin/bash

CURRENT=$(echo $(/usr/bin/xrandr -q --verbose | sed -n '/^.*Brightness:/s/.*: //p' | head -1)*100 | bc -l )
if [ "$1" == "-dec" ] ; then
    let X=(${CURRENT/\.*/}-${2/\-/})%101
elif [ "$1" == "-inc" ] ; then
    let X=(${CURRENT/\.*/}+${2/\-/})
else
    echo "Current Brightness: ${CURRENT}%"
    exit 0
fi

if [ $X -lt 0 ]; then
    X=0
elif [ $X -gt 100 ] ; then
    X=100
fi

if [ "$X" != "" ] ; then
    /usr/bin/xrandr --output DP-3.1 --brightness $(echo ${X}/100 | bc -l )
    echo "Set brighness to ${X}%"
else
    echo "Error"
fi
