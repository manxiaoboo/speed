import yolo_models.detect_target as detect_target
import utils.util as util
import utils.target_order as do
import local_status

def onImageReceived(frame):
    print("GoBack Handler:: RUNING")
    do.nextOutlookPosition()
    local_status.setCamera('0')
    do.ahead(-40, 4)
    return True
    

def missAll():
    do.back()
    return False