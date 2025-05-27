import enums
from blinker import signal

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
NORMAL_LINE_WIDTH = 83
MQTT_READY = False
CAMERA_READY = False
MQTT_CLIENT = None
DETECT_LINE_MODEL = None
DETECT_TARGET_MODEL = None
TARGET_1 = 'A'
TARGET_2 = '3'
CAR_STATUS = enums.Status.LINE1
CAR_BUSY = False
CURR_IMG_BASE_64 = None


img_updated = signal("img_updated")

def updateImage(img):
    global CURR_IMG_BASE_64
    CURR_IMG_BASE_64 = img
    if not CAR_BUSY:
        img_updated.send(img)

def isIDLE():
    return CAR_STATUS == enums.Status.IDLE

def isLINE1():
    return CAR_STATUS == enums.Status.LINE1

def isLINE2():
    return CAR_STATUS == enums.Status.LINE2

def isLINE3():
    return CAR_STATUS == enums.Status.LINE3

def isLINE4():
    return CAR_STATUS == enums.Status.LINE4

def isLINE5():
    return CAR_STATUS == enums.Status.LINE5

def isFindABC():
    return CAR_STATUS == enums.Status.FindABC

def isFind123():
    return CAR_STATUS == enums.Status.Find123