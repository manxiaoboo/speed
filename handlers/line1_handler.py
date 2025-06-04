import sys
import enums
import yolo_models.detect_line as detect_line
import utils.util as util
import utils.direction_order as do

def onImageReceived(frame):
    print("Line1 Handler:: RUNING")
    results = detect_line.predict(frame)
    
    if (tpEntity := util.findTurningPoint(results)):
        isTurning = do.handleTurning(tpEntity, 'left')
    
        if isTurning:
            return True
        else:
            return False
        
    elif (lineEntity := util.findLine(results)):
        do.handleLine(lineEntity)
        return False
    else:
        missAll()

def missAll():
    print("miss all")
    do.back()
    return False
    # sys.exit(0)