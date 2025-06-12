import sys
import yolo_models.detect_target as detect_target
import utils.util as util
import utils.target_order as do
import local_status

def onImageReceived(frame):
    print("FindABC Handler:: RUNING")
    results = detect_target.predict(frame)
    if (targetEntity := util.findTargetABC(results, local_status.TARGET_ABC)):
        print(targetEntity)
        return do.goToABCTarget(targetEntity)
    elif (abcEntities := util.findAllABC(results)):
        print(abcEntities)
        do.nextOutlookPosition(abcEntities)
        return False
    else:
        missAll()

def missAll():
    print("miss all")
    do.left()
    do.back()
    return False