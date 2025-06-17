import yolo_models.detect_target as detect_target
import utils.util as util
import utils.target_order as do
import local_status

def onImageReceived(frame):
    print("Find123 Handler:: RUNING")
    results = detect_target.predict(frame)
    if (targetEntity := util.findTarget123(results, local_status.TARGET_123)):
        
        isDone = do.goTo123Target(targetEntity)
        
        if isDone:
            do.nextOutlookPosition()
            local_status.setCamera('0')
            return True
        else:
            return False
    else:
        missAll()
    

def missAll():
    do.back()
    return False