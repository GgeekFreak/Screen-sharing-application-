#!/usr/bin/env python
"""Webcam video streaming



Using OpenCV to capture frames from webcam.
Compress each frame to jpeg and save it.
Using socket to read from the jpg and send
it to remote address.
!!!press q to quit!!!
"""
import numpy as np
import cv2
from socket import *
import pyscreenshot as ImageGrab
import time
ratio = 1
    
host = "192.168.137.1"
port = 4040
addr = (host, port)
buf = 1024

def sendFile(fName):
    print('send')
    s = socket(AF_INET, SOCK_DGRAM)

    s.sendto(fName, addr)
    f = open(fName, "rb")
    data = f.read(buf)
    while data:
        if(s.sendto(data, addr)):
            data = f.read(buf)
    f.close()
    s.close()

def captureFunc():
    count = 0
    while(True):
        frame = ImageGrab.grab()
        if not frame is None:
            frame = np.array(frame)
            frame = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)
            count = count + 1
            if count == ratio:
                cv2.imwrite("img.jpg", frame)
                sendFile("img.jpg")
                count = 0            
            
        else:
            pass
        time.sleep(1)

if __name__ == '__main__':
    captureFunc()
    cap.release()
    cv2.destroyAllWindows()
