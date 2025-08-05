import yolo_models.detect_line as detect_line
import utils.util as util
import utils.line_order as do

def onImageReceived(frame):
    print("Line5 Handler:: RUNING")
    results = detect_line.predict(frame)
     
    if (lineEntity := util.findEnd(results)):
        do.ahead(-62, 4)
        return True
     
    if (lineEntity := util.findLine(results)):
        do.handleLine(lineEntity)
        return False
    
    else:
        missAll()

def missAll():
    print("miss all")
    do.back()
    return False