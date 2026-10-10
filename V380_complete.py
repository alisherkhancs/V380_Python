#!/usr/bin/env python

import sys
import requests
from time import sleep
import cv2  # type: ignore

# Windows compatibility for getch
try:
    import msvcrt
    def get_key():
        return msvcrt.getch().decode('utf-8', errors='ignore')
except ImportError:
    try:
        import importlib
        _getch = importlib.import_module('getch')
        def get_key():
            return _getch.getch()
    except Exception:
        def get_key():
            return input()

cam = cv2.VideoCapture("rtsp://admin:admin7@192.168.0.131/live/ch00_1")

cv2.namedWindow("test")

img_counter = 0

# Set the name of the XML file.
xml_up = "postup.xml"
xml_down = "postdown.xml"
xml_left = "postleft.xml"
xml_right = "postright.xml"
xml_stop = "poststop.xml"

headers = {'Content-Type': 'text/xml'}

while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("test", frame)
    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = f"opencv_frame_{img_counter}.png"
        cv2.imwrite(img_name, frame)
        print(f"{img_name} written!")
        img_counter += 1
    elif k % 256 == 105:  # 'i' -> Up
        try:
            with open(xml_up) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
            sleep(0.5)
            with open(xml_stop) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
        except Exception as e:
            print(f"PTZ Error: {e}")
    elif k % 256 == 44:  # ',' -> Down
        try:
            with open(xml_down) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
            sleep(0.5)
            with open(xml_stop) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
        except Exception as e:
            print(f"PTZ Error: {e}")
    elif k % 256 == 106:  # 'j' -> Left
        try:
            with open(xml_left) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
            sleep(0.5)
            with open(xml_stop) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
        except Exception as e:
            print(f"PTZ Error: {e}")
    elif k % 256 == 108:  # 'l' -> Right
        try:
            with open(xml_right) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
            sleep(0.5)
            with open(xml_stop) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
        except Exception as e:
            print(f"PTZ Error: {e}")
    elif k % 256 == 107:  # 'k' -> Stop
        try:
            with open(xml_stop) as xml:
                requests.post('http://192.168.0.131:8899/onvif/ptz', data=xml, headers=headers)
        except Exception as e:
            print(f"PTZ Error: {e}")

cam.release()
cv2.destroyAllWindows()
