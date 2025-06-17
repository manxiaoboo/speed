import sys
import yolo_models.detect_target as detect_target
import utils.util as util
import utils.target_order as do
import local_status

def onImageReceived(frame):
    print("FindABC Handler:: RUNING")
    results = detect_target.predict(frame)
    if (targetEntity := util.findTargetABC(results, local_status.TARGET_ABC)):
        do.goToABCTarget(targetEntity)
        return True

    if (util.findALL123(results)):
        return True

    if (util.findAllABC(results)):
        do.nextOutlookPosition()
        return False
        
    missAll()

def missAll():
    print("miss all")
    if (local_status.OUTLOOK[local_status.CURRENT_OUTLOOK_INDEX] == 'left'):
        do.left()
    else:
        do.back()
    return False