from handlers import back_line5_handler, idle_handler, line1_handler, line2_handler, line3_handler, line4_handler, findABC_handler, find123_handler, back_line1_handler, back_line2_handler, back_line3_handler, back_line4_handler, line5_handler, goback_handler
import time
import cv2
import enums
import local_status
import servers.camera_server as camera_server

def next():
        if local_status.isFindABC() or local_status.isFind123():
            local_status.setCamera('2')
        else:
            local_status.setCamera('0')
            
        img = camera_server.takePhoto()
        frame = camera_server.process_image_from_misleading_response(img)
        # cv2.imshow('car', frame)
        # cv2.waitKey(0)
        if local_status.isIDLE():
            idle_handler.onImageReceived(frame)
            time.sleep(3)
        elif local_status.isLINE1():
            isDone = line1_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE2)
        elif local_status.isLINE2():    
            isDone = line2_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE3)
        elif local_status.isLINE3():    
            isDone = line3_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE4)
        elif local_status.isLINE4():    
            isDone = line4_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.LINE5)
        elif local_status.isLINE5():
            isDone = line5_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.FindABC)
                local_status.setCamera('2')
                time.sleep(2)
                camera_server.takePhoto()
        elif local_status.isFindABC():  
            isDone = findABC_handler.onImageReceived(frame)
            if isDone:
                local_status.OFFSET = 0
                setStatus(enums.Status.Find123)
        elif local_status.isFind123():
            isDone = find123_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.GO_BACK)
        elif local_status.isGoBack():
            isDone = goback_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.BACK_LINE1)
        elif local_status.isBACK_LINE1():
            isDone = back_line1_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.BACK_LINE2)
        elif local_status.isBACK_LINE2():    
            isDone = back_line2_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.BACK_LINE3)
        elif local_status.isBACK_LINE3():    
            isDone = back_line3_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.BACK_LINE4)
        elif local_status.isBACK_LINE4():    
            isDone = back_line4_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.BACK_LINE5)
        elif local_status.isBACK_LINE5():    
            isDone = back_line5_handler.onImageReceived(frame)
            if isDone:
                setStatus(enums.Status.IDLE)
        else:
            time.sleep(1)
        
        next()
            
def setStatus(status):
    local_status.CAR_STATUS = status