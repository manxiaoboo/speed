import sys
import enums
import yolo_models.detect_line as detect_line
import utils.util as util
import utils.line_order as do

def onImageReceived(frame):
    print("Line5 Handler:: RUNING")
    
    results = detect_line.predict(frame, 0.02)
        
    if (endEntity := util.findEnd(results)):
            return do.handleEnd(endEntity)
            
    elif (lineEntity := util.findLine(results)):
                do.handleLine(lineEntity, -60, 1)
                return False    
    else:
                missAll()

def missAll():
    print("miss all")
    do.back()
    return False