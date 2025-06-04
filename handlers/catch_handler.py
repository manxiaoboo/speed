import sys
import yolo_models.detect_target as detect_target
import utils.util as util
import utils.target_order as do
import local_status

def onImageReceived(frame):
    print("Find123 Handler:: RUNING")
    do.doCatch()
    missAll()
    

def missAll():
    print("miss all")
    sys.exit(0)
    return False