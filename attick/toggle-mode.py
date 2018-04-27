#!/usr/bin/python
from __future__ import print_function
import Xlib.display
import sys
sys.exit(0)
ms_recall_block=15000
toggle_first=2

import Xlib.rdb

with open('/proc/uptime', 'r') as f:
    uptime_ms = float(f.readline().split()[0]) * 1000


screen_info = Xlib.display.Display().screen().root.xrandr_get_screen_info()
if __name__ == "__main__":
    if (uptime_ms - screen_info.timestamp) > ms_recall_block:
        set_to = (screen_info.size_id + 1 )%toggle_first

        print("Setting mode to ", set_to)
        Xlib.display.Display().screen().root.xrandr_1_0set_screen_config(
                set_to, 1, screen_info.config_timestamp
        )
    else:
        print("Not enough time elapsed")
    sys.exit(0)






