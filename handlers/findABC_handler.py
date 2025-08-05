import sys
import yolo_models.detect_target as detect_target
import utils.util as util
import utils.target_order as do
import local_status

targets = 'ABC'

def onImageReceived(frame):
    print("FindABC Handler:: RUNING")
    global targets
    
    if local_status.OUTLOOK[1] == '':
        results = detect_target.predict(frame, 0.1)
        targetA = util.findA(results)
        targetB = util.findB(results)
        targetC = util.findC(results)
        if targetA:
            local_status.OUTLOOK[1] = 'A'
            targets = targets.replace('A', '')
            do.handleOffsetH(targetA)
            do.move_car('turn', 40, 0.6, 'right')
        elif targetB:
            local_status.OUTLOOK[1] = 'B'
            targets = targets.replace('B', '')
            do.handleOffsetH(targetB)
            do.move_car('turn', 40, 0.6, 'right')
        elif targetC:
            local_status.OUTLOOK[1] = 'C'
            targets = targets.replace('C', '')
            do.handleOffsetH(targetC)
            do.move_car('turn', 40, 0.6, 'right')
        else:
            do.bounce()
            return False
        
        return False
    
    if local_status.OUTLOOK[2] == '':
        results = detect_target.predict(frame, 0.1)
        targetA = util.findA(results)
        targetB = util.findB(results)
        targetC = util.findC(results)
        if targetA:
            local_status.OUTLOOK[2] = 'A'
            targets = targets.replace('A', '')
            do.move_car('turn', 40, 0.6, 'left')
        elif targetB:
            local_status.OUTLOOK[2] = 'B'
            targets = targets.replace('B', '')
            do.move_car('turn', 40, 0.6, 'left')
        elif targetC:
            local_status.OUTLOOK[2] = 'C'
            targets = targets.replace('C', '')
            do.move_car('turn', 40, 0.6, 'left')
        else:
            do.bounce()
            return False
                
        return False
        
    if local_status.OUTLOOK[1] != '' and local_status.OUTLOOK[2] != '':
        local_status.OUTLOOK[0] = targets        
    
    if local_status.OUTLOOK[0] != '' and local_status.OUTLOOK[1] != '' and local_status.OUTLOOK[2] != '':
        print(local_status.OUTLOOK)
        
        if local_status.OUTLOOK[0] == local_status.TARGET_ABC:
            do.move_car('turn', 40, 0.6, 'left')
        elif local_status.OUTLOOK[2] == local_status.TARGET_ABC:
            do.move_car('turn', 40, 0.6, 'right')
            
        do.move_car('ahead', 60, 2)
        return True
    else:
        return False
    

def missAll():
    print("miss all")
    if (local_status.OUTLOOK[local_status.CURRENT_OUTLOOK_INDEX] == 'left'):
        do.left()
    else:
        do.back()
    return False