import sys
import enums
import yolo_models.detect_line as detect_line
import utils.util as util
import utils.direction_order as do

def onImageReceived(frame):
    print("Idle Handler:: RUNING")
    results = detect_line.predict(frame)
    print(results)