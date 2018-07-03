import win32api, win32con
import numpy as np
import time
'''
Author: Devin B, dpb246

Prints pixel location of the mouse every second
used to configure the clicking for the website interface
'''
while True:
    time.sleep(1)
    x,y = win32api.GetCursorPos()
    print("row:", x, "column:", y)
