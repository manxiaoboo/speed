import sys
import enums
import yolo_models.detect_line as detect_line
import utils.util as util
import utils.line_order as do

firstRun = True

def onImageReceived(frame):
    print("Line3 Handler:: RUNING")
    global firstRun
    results = detect_line.predict(frame)
    
    if firstRun == True:
        do.handleOffset(util.findLine(results))
        do.ahead(-55, 2)
        firstRun = False
        return False
    else:
        results = detect_line.predict(frame)
        
        if (tpEntity := util.findTurningPoint(results)):
            isTurning = do.handleTurning(tpEntity, 'right')
        
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