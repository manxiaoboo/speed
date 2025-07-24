import enums
from blinker import signal

IMAGE_URL = "http://192.168.1.5:5000/video_feed?id="
CAMERA_INDEX = '0'

TARGET_ABC = 'B'
TARGET_123 = '1'
CAR_STATUS = enums.Status.LINE1
OUTLOOK = ['left', 'right', 'right', 'left']
CURRENT_OUTLOOK_INDEX = 0


IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
NORMAL_LINE_WIDTH = 83
MQTT_READY = False
CAMERA_READY = False
MQTT_CLIENT = None
DETECT_LINE_MODEL = None
DETECT_TARGET_MODEL = None

CAR_BUSY = False
CURR_IMG_BASE_64 = None
CURRENT_SPRINT_COUNT = 0

img_updated = signal("img_updated")

def getImageUrl():
    print(IMAGE_URL + "" + CAMERA_INDEX)
    return IMAGE_URL + "" + CAMERA_INDEX

def setCamera(index):
    global CAMERA_INDEX
    CAMERA_INDEX = index

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

def isBACK_LINE1():
    return CAR_STATUS == enums.Status.BACK_LINE1

def isBACK_LINE2():
    return CAR_STATUS == enums.Status.BACK_LINE2

def isBACK_LINE3():
    return CAR_STATUS == enums.Status.BACK_LINE3

def isBACK_LINE4():
    return CAR_STATUS == enums.Status.BACK_LINE4

def isBACK_LINE5():
    return CAR_STATUS == enums.Status.BACK_LINE5

def isFindABC():
    return CAR_STATUS == enums.Status.FindABC

def isFind123():
    return CAR_STATUS == enums.Status.Find123

def isCatch():
    return CAR_STATUS == enums.Status.Catch

def isGoBack():
    return CAR_STATUS == enums.Status.GO_BACK