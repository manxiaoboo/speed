import yolo_models.detect_line as detect_line
import utils.util as util
import utils.line_order as do
import local_status

def onImageReceived(frame):
    print("Line5 Handler:: RUNING")
    results = detect_line.predict(frame)
     
    if local_status.CURRENT_SPRINT_COUNT == 6:
        do.ahead(-52, 6)
        return True
     
    if (lineEntity := util.findLine(results)):
        do.handleLine(lineEntity)
        local_status.CURRENT_SPRINT_COUNT = local_status.CURRENT_SPRINT_COUNT + 1
        return False
    
    else:
        missAll()

def missAll():
    print("miss all")
    do.back()
    return False