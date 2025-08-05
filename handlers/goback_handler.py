import yolo_models.detect_target as detect_target
import utils.util as util
import utils.target_order as do
import local_status

def onImageReceived(frame):
    print("GoBack Handler:: RUNING")
    
    if local_status.OFFSET > 0:
        do.offsetHorizontal(35, abs(local_status.OFFSET), 'left')
        
    if local_status.OFFSET < 0:
        do.offsetHorizontal(35, abs(local_status.OFFSET), 'right')
    
    do.ahead(-60, 2.8)
    
    if local_status.OUTLOOK[0] == local_status.TARGET_ABC:
        do.move_car('turn', 42, 0.6, 'right')
    elif local_status.OUTLOOK[2] == local_status.TARGET_ABC:
        do.move_car('turn', 42, 0.6, 'left')
    
    do.ahead(-60, 2)
    
    return True
    

def missAll():
    do.back()
    return False