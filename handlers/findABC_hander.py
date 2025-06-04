import sys
import yolo_models.detect_line as detect_line
import utils.util as util
import utils.direction_order as do

def onImageReceived(frame):
    print("FindABC Handler:: RUNING")
    sys.exit(0)

def missAll():
    print("miss all")
    do.back()
    return False