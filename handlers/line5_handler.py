import sys
import enums
import yolo_models.detect_line as detect_line
import utils.util as util
import utils.line_order as do

firstRun = True
needFixOffset = False

def onImageReceived(frame):
    print("Line5 Handler:: RUNING")
    global firstRun
    global needFixOffset
    
    if firstRun == True:
        do.ahead(-55, 3.5)
        firstRun = False
        return False
    else:
        results = detect_line.predict(frame)
        
        if needFixOffset == True:
            lineEntity = util.findLine(results)
            return do.handleOffset(lineEntity)
        else:
            if (endEntity := util.findEnd(results)):
                turned = do.handleEnd(endEntity)
                if (turned):
                    needFixOffset = True
                    return False
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